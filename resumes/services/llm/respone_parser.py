import json
import re


def clean_json_string(raw_output: str) -> str:
    # Remove JS-style comments
    raw_output = re.sub(r"//.*", "", raw_output)

    # Remove trailing commas before } or ]
    raw_output = re.sub(r",\s*}", "}", raw_output)
    raw_output = re.sub(r",\s*]", "]", raw_output)

    return raw_output.strip()


def parse_llm_json(raw_output: str):
    try:
        cleaned = clean_json_string(raw_output)
        return json.loads(cleaned)
    except Exception:
        return {
            "error": "Invalid JSON from model",
            "raw_output": raw_output,
        }
