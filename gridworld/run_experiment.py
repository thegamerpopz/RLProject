import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from gridworld.advice import beliefs_from_advice, classify_false_claims, make_advice
from gridworld.agents import Explorer
from gridworld.beliefs import Beliefs
from gridworld.env import GridWorld, new_game
from gridworld.expriment import run_episodes

BUDGETS = (1, 3, 10)
LEARNERS = ("calibrated", "literal")


def rng_for(*key):
    return np.random.default_rng(np.random.SeedSequence(list(key)))


def run_game(game, seed):
    roles = new_game(game)
    level_seeds = rng_for(seed, game, 1).integers(0, 2 ** 32, size=10)  # shared by all conditions
    conditions = [("no_advice", 0, []),
                  ("oracle", 0, make_advice(Beliefs(), "oracle", true_roles=roles))]
    events = []
    for E in BUDGETS:  # advisor plays E episodes on its own levels
        advisor = Explorer(Beliefs(), rng_for(seed, game, 2, E))
        meta = {"game": game, "condition": "advisor", "budget": E,
                "agent": "advisor", "learner_type": "none"}
        _, ev = run_episodes(GridWorld(roles), advisor,
                             rng_for(seed, game, 3, E).integers(0, 2 ** 32, size=E), meta)
        events += ev
        for mode in ("best_guess", "selective"):
            conditions.append((mode, E, make_advice(advisor.beliefs, mode)))

    rows = []
    for learner in LEARNERS:
        for cond, E, advice in conditions:
            beliefs = beliefs_from_advice(advice, literal=(learner == "literal"))
            explorer = Explorer(beliefs, rng_for(seed, game, 4))
            meta = {"game": game, "condition": cond, "budget": E,
                    "agent": "learner", "learner_type": learner}
            result, ev = run_episodes(GridWorld(roles), explorer, level_seeds, meta)
            c = classify_false_claims(advice, roles, ev)
            rows.append({"learner": learner, "budget": E, "condition": cond,
                         "won_any": int(result["won_any"]), "first_win": result["first_win"],
                         "deaths": result["deaths"],
                         "warning_touched": c["warning"]["touched_later"],
                         "warning_never": c["warning"]["never_touched"],
                         "endorsement_touched": c["endorsement"]["touched_later"],
                         "endorsement_never": c["endorsement"]["never_touched"]})
            events += ev
    return rows, events


def summarize(rows):
    groups = defaultdict(list)
    for r in rows:
        groups[(r["learner"], r["budget"], r["condition"])].append(r)
    out = []
    for (learner, budget, cond), rs in groups.items():
        row = {"learner": learner, "budget": budget, "condition": cond, "n_games": len(rs)}
        for m in ("won_any", "first_win", "deaths"):
            v = np.array([r[m] for r in rs], dtype=float)
            row[m + "_mean"], row[m + "_se"] = v.mean(), v.std(ddof=1) / np.sqrt(len(v))
        for k in ("warning_touched", "warning_never", "endorsement_touched", "endorsement_never"):
            row[k] = sum(r[k] for r in rs)
        out.append(row)
    return out


def plot(summary, path):
    get = {(r["learner"], r["budget"], r["condition"]): r for r in summary}
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for ax, learner in zip(axes, LEARNERS):
        for cond, color in (("no_advice", "gray"), ("oracle", "green")):
            r = get[(learner, 0, cond)]
            ax.axhline(r["first_win_mean"], color=color, ls="--", label=cond)
        for cond in ("best_guess", "selective"):
            rs = [get[(learner, E, cond)] for E in BUDGETS]
            ax.errorbar(BUDGETS, [r["first_win_mean"] for r in rs],
                        yerr=[1.96 * r["first_win_se"] for r in rs],
                        marker="o", capsize=3, label=cond)
        ax.set_title(f"{learner} learner")
        ax.set_xlabel("advisor budget E")
        ax.set_xticks(BUDGETS)
    axes[0].set_ylabel("mean first-win episode (11 = never)")
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--games", type=int, default=100)
    args = parser.parse_args()

    Path("results").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    rows = []
    for game in range(args.games):
        game_rows, events = run_game(game, args.seed)
        rows += game_rows
        with open(f"logs/game_{game:03d}.jsonl", "w") as f:
            f.writelines(json.dumps(e) + "\n" for e in events)

    summary = summarize(rows)
    with open("results/summary.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    plot(summary, "results/first_win.png")
    print("wrote results/summary.csv, results/first_win.png, logs/")


if __name__ == "__main__":
    main()