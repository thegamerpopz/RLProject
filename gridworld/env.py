import numpy as np
SEED=31121
ROLES = ("LETHAL", "REWARD", "GOAL", "NEUTRAL")
COLORS = ("RED", "GREEN", "BLUE", "YELLOW", "PURPLE")
ACTIONS = ("UP", "DOWN", "LEFT", "RIGHT")
DIRECTIONs=((1,0),(-1,0),(0,-1),(0,1))
COLOR_CODE = {c: 3 + i for i, c in enumerate(COLORS)}  # RED=3 GREEN=4 BLUE=5 YELLOW=6 PURPLE=7
CODE_TO_COLOR = {v: k for k, v in COLOR_CODE.items()}

def new_game(seed: int) -> dict[str, str]:
    np.random.seed(seed)
    maps: dict[str, str] = {}
    goal_colour=str(np.random.choice(COLORS))
    maps[goal_colour] = "GOAL"
    remaining=[c for c in COLORS if c!=goal_colour]
    lethal_colour=str(np.random.choice(remaining))
    maps[lethal_colour] = "LETHAL"
    remaining.remove(lethal_colour)
    for color in remaining:
        maps[color] = np.random.choice( ("LETHAL", "REWARD", "NEUTRAL"))
    return maps




class GridWorld:
    def _has_safe_path(self, level, start, goal_codes, lethal_codes) -> bool:
        queue = [start]
        head = 0
        visited = {start}
        while head < len(queue):
            r, c = queue[head]
            head += 1
            if level[r][c] in goal_codes:
                return True
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if (nr, nc) in visited:
                    continue
                if level[nr][nc] == 1:  # wall
                    continue
                if level[nr][nc] in lethal_codes:  # lethal object
                    continue
                visited.add((nr, nc))
                queue.append((nr, nc))
        return False
    def __init__(self,size=7, objects_per_color=(1, 3),
 p_effect=0.85, p_accident=0.05, max_steps=50):
        self.size=size
        self.objects_per_color=objects_per_color
        self.p_effect=p_effect
        self.p_accident=p_accident
        self.max_steps=max_steps
        self.maps=new_game(SEED)

    def reset(self, seed: int) -> np.ndarray:
        np.random.seed(seed)
        while True:
            n=self.size
            level=np.ones((n,n), dtype=int)
            grid = np.zeros((n - 2, n - 2), dtype=int)
            no_of_objects= np.random.randint(1, 4, size=5)
            total_objects= np.sum(no_of_objects)
            positions = np.random.choice(grid.size, size=total_objects + 1, replace=False)
            positions = np.column_stack(np.unravel_index(positions, grid.shape))
            avatar_pos = positions[-1]
            grid[avatar_pos[0], avatar_pos[1]] = 2
            positions= positions[:-1]
            color_codes = np.repeat(list(COLOR_CODE.values()), no_of_objects)
            for (row, col), code in zip(positions, color_codes):
                grid[row, col] = code
            for i in range(1,n-1):
                for j in range(1,n-1):
                    level[i][j]=grid[i-1][j-1]
            avatar_pos = (int(avatar_pos[0]) + 1, int(avatar_pos[1]) + 1)
            lethal_codes = {COLOR_CODE[c] for c, r in self.maps.items() if r == "LETHAL"}
            goal_codes = {COLOR_CODE[c] for c, r in self.maps.items() if r == "GOAL"}
            if self._has_safe_path(level, avatar_pos, goal_codes, lethal_codes):
                return level


    def step(self,level, action: str) -> tuple[np.ndarray, int, bool, dict]:
        move = dict(zip(ACTIONS, DIRECTIONS))


    def render(self, level) -> str:
        lines = []
        for i in range(7):
            row = ""
            for j in range(7):
                if level[i][j] == 0:
                    row += "."
                if level[i][j] == 1:
                    row += "#"
                if level[i][j] == 2:
                    row += "@"
                if level[i][j] == 3:
                    row += CODE_TO_COLOR[3][:1]
                if level[i][j] == 4:
                    row += CODE_TO_COLOR[4][:1]
                if level[i][j] == 5:
                    row += CODE_TO_COLOR[5][:1]
                if level[i][j] == 6:
                    row += CODE_TO_COLOR[6][:1]
                if level[i][j] == 7:
                    row += CODE_TO_COLOR[7][:1]
            lines.append(row)
        return "\n".join(lines)





a=GridWorld()
b=a.reset(seed=SEED)
print(a.render(level=b))