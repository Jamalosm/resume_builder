import re


ACTION_VERBS = [
    "developed", "implemented", "designed",
    "optimized", "improved", "built", "created"
]


def score_bullet(bullet: str) -> int:
    score = 0
    text = bullet.lower()

    if any(verb in text for verb in ACTION_VERBS):
        score += 30

    if re.search(r"\d+%|\d+", bullet):
        score += 30

    if len(bullet.split()) > 8:
        score += 20

    score += 20  # base clarity

    return min(score, 100)
