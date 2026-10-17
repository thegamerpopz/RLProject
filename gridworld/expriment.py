def run_episodes(world, explorer, level_seeds, metadata):
    if len(level_seeds) == 0:
        raise ValueError("At least one episode is required")

    events = []
    outcomes = []
    for episode, seed in enumerate(level_seeds, start=1):
        obs = world.reset(int(seed))
        done = False
        while not done:
            obs, _, done, info = world.step(explorer.act(obs))
            explorer.observe(info["events"])
            for event in info["events"]:
                events.append({**metadata, "episode": episode, **event})
        outcomes.append(info["events"][-1]["outcome"])

    summary = {
        "won_any": "win" in outcomes,
        "first_win": outcomes.index("win") + 1 if "win" in outcomes else len(outcomes) + 1,
        "deaths": outcomes.count("death"),
    }
    return summary, events