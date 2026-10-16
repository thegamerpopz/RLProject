import numpy as np
from env import COLOR_CODE
from beliefs import Beliefs
from constants import *
class Explorer:
 def __init__(self, beliefs: Beliefs, rng: np.random.Generator,
 danger_threshold=0.5):
  self.beliefs = beliefs
  self.rng = rng
  self.danger_threshold = danger_threshold
 def _pick(self, options):
  return options[self.rng.integers(len(options))]

 def _distances(self, grid, start):
  # Count steps from start to every cell using allowed cells
  # dist[row, col] = steps needed, or -1 if the cell can't be reached.
  dist = np.full(grid.shape, -1, dtype=int) #array that stores distance
  dist[start] = 0
  queue = [start]
  head = 0
  while head < len(queue):
   r, c = queue[head]
   head += 1
   for dr, dc in DIRECTIONS:
    nr, nc = r + dr, c + dc
    if grid[nr, nc] == 1 or dist[nr, nc] != -1:
     continue
    dist[nr, nc] = dist[r, c] + 1
    queue.append((nr, nc))
  return dist

 def shortest_path(self, grid, obs, start, colors):
  # group every object ofx` color together as a target
  codes = [COLOR_CODE[color] for color in colors]
  targets = []
  for row in range(len(obs)):
   for col in range(len(obs)):
    if obs[row][col] in codes:
     targets.append((row, col))
  #min distance of a target from start
  dist = self._distances(grid, start)
  nearest_dist = -1
  for t in targets:
   if dist[t] > 0 and (dist[t] < nearest_dist):
    nearest_dist = dist[t]
  if nearest_dist is -1:
   return None
  nearest_points = [t for t in targets if dist[t] == nearest_dist]
  target = self._pick(nearest_points)

  #what step to take towards the target point from starting point
  back = self._distances(grid, target)
  moves = []
  for i,direction in enumerate(DIRECTIONS):
   row=start[0]+direction[0]
   col=start[1]+direction[1]
   if back[row,col] == back[start] - 1:
    moves.append(ACTIONS[i])
  return self._pick(moves)

 def act(self, obs: np.ndarray) -> str:
  avatar_pos=np.argwhere(obs == 2)
  start = (int(avatar_pos[0]), int(avatar_pos[1]))
  grid=obs.copy()
  guess=self.beliefs.best_guess()
  dangerous=[]
  goal=[]
  uncertain=[]
  for c in COLORS:
   if guess[c][0]=="LETHAL" and guess[c][1] >= self.danger_threshold:
    dangerous.append(c)
   if guess[c][0] == "GOAL" and guess[c][1] >= 0.5:
     goal.append(c)
   if guess[c][1] < 0.95:  # largest role probability still low
     uncertain.append(c)
  for c in dangerous:
   color_num=COLOR_CODE[c]
   grid[obs==color_num]=1 # we treat the blocked object as wall for the purpose of BFS
  #nearest goal object action
  action = self.shortest_path(grid,obs,start,goal)
  if action is not None:
   return action
  #nearest uncertain object action
  action=self.shortest_path(grid,obs, start,uncertain)
  if action is not None:
   return action
  danger_codes = [COLOR_CODE[c] for c in dangerous]
  options = []
  for i,direction in enumerate(DIRECTIONS):
   row = start[0] + direction[i][0]
   column = start[1] + direction[i][1]
   if obs[row, column] not in danger_codes:
    options.append(ACTIONS[i])
  return self._pick(options)


 def observe(self, events: list[dict]) -> None:
  for e in events:
   if e["type"] == "contact":  # skip episode_end; never read e["cause"]
    self.beliefs.update(e["color"], e["observed"])
