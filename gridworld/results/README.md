# Gridworld with hidden rules

A small testbed where an agent learns the hidden roles of five colors (LETHAL, REWARD,
GOAL, NEUTRAL) by touching them, and where one agent (the advisor) gives advice to
another (the learner). The experiment asks when that advice helps and when it hurts,
including the hot-stove effect: a false warning is never tested, so it is never corrected.

## Requirements

Python 3.10+ with `numpy` and `matplotlib`.

    pip install numpy matplotlib

## How to run

Run everything from the repository root (the folder containing `gridworld/`).

**Full experiment (100 paired games, about 15 seconds):**

    python run_experiment.py --seed 0

Writes:
- `results/summary.csv`: one row per learner, budget and condition, with the mean and
  standard error of `won_any`, `first_win` and `deaths`, plus false-statement counts
  (`warning_touched`, `warning_never`, `endorsement_touched`, `endorsement_never`)
- `results/first_win.png`: mean first-win episode against advisor budget, with
  ±1.96 SE error bars; no-advice and oracle are drawn as horizontal lines
- `logs/game_000.jsonl` to `logs/game_099.jsonl`: one event log per game

The same `--seed` always gives identical results. Use `--games 5` for a quick test.
A budget of 0 in the CSV is a placeholder for `no_advice` and `oracle`, which do not
depend on the advisor's number of episodes. `first_win` = 11 means no win in 10 episodes.

**Hot-stove check (Part F), using the no-advice learner:**

    python hot_stove_check.py                              # p_accident = 0.05
    python hot_stove_check.py --p-accident 0.2 --games 500 # enough accident cases

**Module self-checks:**

    python -m gridworld.beliefs   # Bayes updates
    python -m gridworld.advice    # advice and learner priors
    python -m gridworld.env       # renders one level

## Layout

    gridworld/
      constants.py   roles, colors, actions
      env.py         GridWorld and new_game (hidden roles, noisy effects)
      beliefs.py     Bayesian beliefs over the four roles of each color
      agents.py      Explorer: a fixed rule that acts on its beliefs (BFS paths)
      advice.py      advice modes, learner priors, false-claim classification
      expriment.py   run_episodes
    run_experiment.py    the 100-game paired experiment, summary and plot
    hot_stove_check.py   Denrell hot-stove check
    results/  logs/

## AI tools

I used AI assistance (Claude) in this project. Here is what was done how:

- **Core modules** (`constants.py`, `env.py`, `beliefs.py`, `agents.py`, `advice.py`,
  `expriment.py`): a mix of my own coding and AI help. I was not familiar with
  breadth-first search (BFS), so I learned the logic and cross-checked the AI's
  implementation of it against my understanding.
- **`run_experiment.py` and `hot_stove_check.py`**: written by the AI, not by me. They
  mainly handle the orchestration of the experiment and reading and writing files, which
  I am not familiar with. I only skimmed over them.
- **Questions and understanding**: I also used Claude to explain parts of the code and
  the experiment to me while I prepared this submission.

The results and the conclusions in this repository come from running this code.
