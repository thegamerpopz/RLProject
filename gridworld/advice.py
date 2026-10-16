from .constants import ROLES,COLORS
from .beliefs import Beliefs
LITERAL_CONFIDENCE=0.99
TEMPLATES = {
    "LETHAL": "Touching {color} kills you ({pct}% sure)",
    "REWARD": "Touching {color} gives you a point ({pct}% sure)",
    "GOAL": "Touching {color} wins the level ({pct}% sure)",
    "NEUTRAL": "Touching {color} is harmless ({pct}% sure)",
}
def make_advice(beliefs, mode="best_guess", tau=0.8, true_roles=None) -> list[dict]:
    if mode == "oracle":
        return [{"color": c, "role": true_roles[c], "confidence": 1.0}
                for c in beliefs.colors]
    advice = []
    for color, (role, prob) in beliefs.best_guess().items():
        if mode == "selective" and prob < tau:
            continue
        advice.append({"color": color, "role": role, "confidence": prob})
    return advice
def advice_to_text(advice: list[dict]) -> str:
    if not advice:
        return "No advice."
    lines = []
    for s in advice:
        pct = f"{100 * s['confidence']:.0f}"
        lines.append(TEMPLATES[s["role"]].format(color=s["color"], pct=pct))
    return "\n".join(lines)
def beliefs_from_advice(advice, p_effect=0.85, p_accident=0.05, cap=0.99,
 literal=False) -> Beliefs:
    prior = {}
    for s in advice:
        color, role = s["color"], s["role"]
        if color not in COLORS:
            raise ValueError(f"unknown color {color!r}")
        if role not in ROLES:
            raise ValueError(f"unknown role {role!r}")
        confidence = LITERAL_CONFIDENCE if literal else s["confidence"]
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(f"confidence {confidence} is not in [0, 1]")
        confidence = min(confidence, cap)
        rest = (1 - confidence) / (len(ROLES) - 1)
        prior[color] = {r: (confidence if r == role else rest) for r in ROLES}
    return Beliefs(colors=COLORS, p_effect=p_effect, p_accident=p_accident,
                   prior=prior or None)


# def classify_false_claims(advice, true_roles, learner_events) -> dict:
#     touched = {e["color"] for e in learner_events if e.get("type") == "contact"}
#     counts = {"warning": {"touched_later": 0, "never_touched": 0},
#               "endorsement": {"touched_later": 0, "never_touched": 0}}
#     for s in advice:
#         if s["role"] == true_roles[s["color"]]:
#             continue  # true statement
#         kind = "warning" if s["role"] == "LETHAL" else "endorsement"
#         key = "touched_later" if s["color"] in touched else "never_touched"
#         counts[kind][key] += 1
#     return counts


if __name__ == "__main__":
    b = Beliefs()
    b.update("RED", "death")
    b.update("RED", "death")
    b.update("BLUE", "nothing")
    for mode in ("best_guess", "selective"):
        a = make_advice(b, mode)
        print(mode, a)
        print(advice_to_text(a), "\n")
    print(beliefs_from_advice(make_advice(b)).posterior("RED"))
    print(beliefs_from_advice(make_advice(b), literal=True).posterior("RED"))
