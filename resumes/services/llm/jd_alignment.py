from .llm_client import LLMClient
from .prompt_builder import build_analysis_prompt
from .respone_parser import parse_llm_json
from .ats_scoring import calculate_keyword_score, calculate_section_score
from .bullet_strength import score_bullet
from .skill_gap import find_skill_gap


def align_resume_to_jd(resume_text: str, jd_text: str):
    client = LLMClient()

    # 🔥 Build compact prompt
    prompt = build_analysis_prompt(resume_text, jd_text)

    raw_output = client.generate(prompt)

    ai_result = parse_llm_json(raw_output)

    # 🔥 Hybrid scoring
    keyword_score = calculate_keyword_score(resume_text, jd_text)
    section_score = calculate_section_score(resume_text)

    ai_result["keyword_score"] = keyword_score
    ai_result["section_score"] = section_score

    # 🔥 Bullet scoring (rule-based)
    bullets = resume_text.split("\n")
    bullet_scores = []

    for b in bullets:
        if len(b.strip()) > 10:
            bullet_scores.append({
                "bullet": b,
                "score": score_bullet(b)
            })

    ai_result["bullet_strength"] = bullet_scores[:5]

    # 🔥 Skill gap rule-based
    ai_result["rule_based_skill_gap"] = find_skill_gap(
        resume_text,
        jd_text
    )

    return ai_result
