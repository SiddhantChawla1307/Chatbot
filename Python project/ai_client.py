# ai_client.py
from typing import Optional
import requests
from config import PERPLEXITY_API_KEY

PPLX_URL = "https://api.perplexity.ai/chat/completions"


class PerplexityError(Exception):
    pass


def is_enabled() -> bool:
    return PERPLEXITY_API_KEY is not None and PERPLEXITY_API_KEY.strip() != ""


def get_faqs(question: str) -> str:
    if not is_enabled():
        return "Perplexity API key not configured. Add PERPLEXITY_API_KEY in your .env to enable AI insights."

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    prompt = (
        f"Give me the answer to the questions: {question}"
        f"Remove citations, don't give in fancy markdown. Use plain text format"
        f"Give me a very short answer"
    )

    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "You are a friendly movie expert."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.5,
        "max_tokens": 512,
        "stream": False,
    }
    resp = requests.post(PPLX_URL, headers=headers, json=payload)
    data = resp.json()
    if resp.status_code != 200:
        msg = data.get("error", {}).get("message", "Perplexity API error")
        raise PerplexityError(msg)

    # standard chat completion shape
    try:
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        raise PerplexityError(f"Unexpected API response: {e}")