
import argparse

from gridworld.agents import Explorer
from gridworld.beliefs import Beliefs
from gridworld.env import GridWorld, new_game
from gridworld.expriment import run_episodes
from run_experiment import rng_for


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--games", type=int, default=100)
    parser.add_argument("--p-accident", type=float, default=0.05)
    args = parser.parse_args()

    # counts[group] = [cases, touched_again]
    counts = {"accident_death": [0, 0], "harmless": [0, 0]}
    for game in range(args.games):
        roles = new_game(game)
        level_seeds = rng_for(args.seed, game, 1).integers(0, 2**32, size=10)
        # same setup as the no_advice learner in run_experiment.py, but with
        # the chosen p_accident in both the world and the learner's model
        world = GridWorld(roles, p_accident=args.p_accident)
        explorer = Explorer(Beliefs(p_accident=args.p_accident),
                            rng_for(args.seed, game, 4))
        _, events = run_episodes(world, explorer, level_seeds, {})

        contacts = [e for e in events if e["type"] == "contact"]
        for color, role in roles.items():
            if role != "NEUTRAL":
                continue
            mine = [e for e in contacts if e["color"] == color]
            if not mine:
                continue  # never touched at all: no first contact to classify
            first = mine[0]
            if first["observed"] == "death" and first["cause"] == "accident":
                group = "accident_death"
            elif first["observed"] == "nothing":
                group = "harmless"
            else:
                continue
            counts[group][0] += 1
            counts[group][1] += int(len(mine) > 1)

    print(f"p_accident={args.p_accident}, games={args.games}, seed={args.seed}")
    for group, (cases, again) in counts.items():
        rate = again / cases if cases else float("nan")
        print(f"{group:15s} cases={cases:4d}  touched again={again:4d}  rate={rate:.3f}")
    if counts["accident_death"][0] < 30:
        print("fewer than 30 accident cases: rerun with --p-accident 0.2 ")


if __name__ == "__main__":
    main()
