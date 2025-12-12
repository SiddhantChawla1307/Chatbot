# ai_client.py
import random;
from nltk.stem import WordNetLemmatizer;
from nltk.tokenize import word_tokenize;

import requests;
from config import PERPLEXITY_API_KEY

PPLX_URL = "https://api.perplexity.ai/chat/completions"


class PerplexityError(Exception):
    pass


def is_enabled() -> bool:
    return PERPLEXITY_API_KEY is not None and PERPLEXITY_API_KEY.strip() != ""


def get_faqs(question: str) -> str:
    if not is_enabled():
        return "AI is not configured right now."

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
        "temperature": 0.5,
        "max_tokens": 200,
        "stream": False,
    }

    resp = requests.post(PPLX_URL, headers=headers, json=payload)
    data = resp.json()

       # standard chat completion shape
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        return "Sorry, something went wrong."
    
    lemmatizer = WordNetLemmatizer()

def preprocess(sentence):
    tokens = word_tokenize(sentence.lower())
    return [lemmatizer.lemmatize(word) for word in tokens]

responses = {
    "greeting": ["Hi!", "Hello!", "Hey!"],
    "name": ["I am a chatbot built using NLTK."],
    "farewell": ["Goodbye!", "Bye! See you later."],
    "how_are_you": ["I'm fine 😊"]
}

def get_intent(user_input):
    msg = user_input.lower().strip()

    # SAFE direct checks first (no NLTK)
    if any(word in msg for word in ["hello", "hi", "hey"]):
        return "greeting"
    if "how are you" in msg:
        return "how_are_you"
    if "bye" in msg:
        return "farewell"
    if "name" in msg:
        return "name"

    # Only then try NLTK token logic
    try:
        tokens = preprocess(msg)
        if "hello" in tokens or "hi" in tokens or "hey" in tokens:
            return "greeting"
    except Exception:
        pass

    return "unknown"

# ---------------- ONE FUNCTION FOR GUI ----------------
def get_bot_response(user_input: str) -> str:
    try:
        intent = get_intent(user_input)

        # Rule-based NLTK responses
        if intent in responses:
            return random.choice(responses[intent])

        # AI fallback only if key is configured
        if is_enabled():
            return get_faqs(user_input)

        return "I'm still learning. Please try something else."

    except Exception:
        return "Sorry, something went wrong."


