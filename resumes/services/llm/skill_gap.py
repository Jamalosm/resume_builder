import re


def extract_keywords(text: str):
    return set(re.findall(r"\b[a-zA-Z]{3,}\b", text.lower()))


def find_skill_gap(resume_text: str, jd_text: str):
    resume_skills = extract_keywords(resume_text)
    jd_skills = extract_keywords(jd_text)

    missing = jd_skills - resume_skills

    return list(missing)[:15]
