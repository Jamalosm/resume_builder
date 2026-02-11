import re


def calculate_keyword_score(resume_text: str, jd_text: str) -> float:
    jd_words = set(re.findall(r"\b\w+\b", jd_text.lower()))
    resume_words = set(re.findall(r"\b\w+\b", resume_text.lower()))

    if not jd_words:
        return 0

    matched = jd_words.intersection(resume_words)
    return round((len(matched) / len(jd_words)) * 100, 2)


def calculate_section_score(resume_text: str) -> int:
    score = 0

    if "summary" in resume_text.lower():
        score += 20
    if "skills" in resume_text.lower():
        score += 20
    if "experience" in resume_text.lower():
        score += 20
    if "education" in resume_text.lower():
        score += 20
    if len(resume_text) > 300:
        score += 20

    return score
