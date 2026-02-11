import re


def extract_keywords(text: str):
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    return set(words)


def keyword_match_score(resume_text: str, jd_text: str):
    resume_words = extract_keywords(resume_text)
    jd_words = extract_keywords(jd_text)

    if not jd_words:
        return 0

    matched = resume_words.intersection(jd_words)

    return int((len(matched) / len(jd_words)) * 100)
