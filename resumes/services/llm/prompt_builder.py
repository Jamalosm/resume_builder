def build_analysis_prompt(resume, jd):
    return f"""
You are a JSON generator.

Return STRICT VALID JSON ONLY.
Do NOT add comments.
Do NOT explain.
Do NOT include markdown.
Output must start with {{ and end with }}.

Schema:
{{
  "alignment_score": integer,
  "missing_keywords": list of strings,
  "skill_gap": list of strings,
  "improved_summary": string
}}

Resume:
{resume}

JD:
{jd}
"""
