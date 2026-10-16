from .constants import COLORS, ROLES
class Beliefs:
 def __init__(self, colors=COLORS, p_effect=0.85, p_accident=0.05, prior=None):
  self.colors = tuple(colors)
  self.p_effect = p_effect
  self.p_accident = p_accident
  self.prior = prior
  a=p_accident
  p=p_effect
  self.likelihood = {
   "death": {"LETHAL": a + (1 - a) * p, "REWARD": a, "GOAL": a, "NEUTRAL": a},
   "point": {"LETHAL": 0.0, "REWARD": (1 - a) * p, "GOAL": 0.0, "NEUTRAL": 0.0},
   "win": {"LETHAL": 0.0, "REWARD": 0.0, "GOAL": (1 - a) * p, "NEUTRAL": 0.0},
   "nothing": {"LETHAL": (1 - a) * (1 - p), "REWARD": (1 - a) * (1 - p),
               "GOAL": (1 - a) * (1 - p), "NEUTRAL": 1 - a},
  }
  # probs[color][role] gives the current belief
  self.probs = {c: {r: 1 / len(ROLES) for r in ROLES} for c in self.colors}
  if prior is not None:
   for c in self.colors:
    if c in prior:
     self.probs[c] = {r: prior[c][r] for r in ROLES}

 def update(self, color: str, observed: str) -> None:
  if color not in self.colors:
   raise ValueError(f"Color {color} not in the list of colors")
  else:
   weights = {r: self.probs[color][r] * self.likelihood[observed][r] for r in ROLES}
   total = sum(weights.values())
   self.probs[color] = {r: w / total for r, w in weights.items()}

 def posterior(self, color: str) -> dict[str, float]:
  return dict(self.probs[color])
 def best_guess(self) -> dict[str, tuple[str, float]]:
  guesses = {}
  for c in self.colors:
   best_role=None
   best_prob = -1
   for r in ROLES:
    if self.probs[c][r] > best_prob:
     best_role = r
     best_prob = self.probs[c][r]
    guesses[c] = (best_role, best_prob)
  return guesses
if __name__ == "__main__":
    b = Beliefs()
    b.update(color="BLUE",observed="nothing")
    print(b.posterior("BLUE"))
    b.update(color="BLUE",observed="nothing")
    print(b.posterior("BLUE"))

    b = Beliefs()
    b.update(color="RED", observed="death")
    print(b.posterior("RED"))
    b.update(color="RED", observed="death")
    print(b.posterior("RED"))
