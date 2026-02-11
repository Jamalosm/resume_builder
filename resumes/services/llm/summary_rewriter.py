from .llm_client import LLMClient


def rewrite_summary(summary_text: str):
    prompt = f"""
Rewrite this resume summary professionally.
Max 80 words.
ATS optimized.

{summary_text}
"""

    client = LLMClient()
    return client.generate(prompt)
