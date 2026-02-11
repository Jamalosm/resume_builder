import requests


class LLMClient:
    BASE_URL = "http://localhost:11434/api/generate"

    def __init__(self):
        self.session = requests.Session()

    def generate(self, prompt: str) -> str:
        response = self.session.post(
            self.BASE_URL,
            json={
                "model": "phi3:mini",
                "prompt": prompt,
                "stream": False,
                "keep_alive": "10m",   # 🔥 keeps model in RAM
                "options": {
                    "temperature": 0.1,
                    "num_predict": 100,   # 🔥 reduce more
                    "top_k": 20,
                    "top_p": 0.8,
                },
            },
            timeout=120,
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Ollama Error {response.status_code}: {response.text}"
            )

        return response.json().get("response", "").strip()
