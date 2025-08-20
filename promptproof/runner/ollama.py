from __future__ import annotations
import httpx
import json
import os

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

class OllamaError(RuntimeError):
    pass

def _post_json(path: str, payload: dict) -> dict:
    url = f"{OLLAMA_URL}{path}"
    try:
        # Keep timeouts short so we never “hang”
        with httpx.Client(timeout=httpx.Timeout(connect=5.0, read=20.0, write=10.0, pool=5)) as c:
            r = c.post(url, json=payload)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise OllamaError(f"Ollama request failed: {e}")

def generate_text(model: str, prompt: str, temperature: float = 0.3, max_tokens: int = 80) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens
        }
    }
    data = _post_json("/api/generate", payload)
    return data.get("response", "")

def generate_json(model: str, system: str, user: str, schema_hint: str, temperature: float = 0.3, max_tokens: int = 80) -> dict:
    prompt = (
        f"{system}\n\n"
        f"{user}\n\n"
        "Respond ONLY as strict JSON compatible with this schema idea:\n"
        f"{schema_hint}\n"
        "No prose. No markdown. JSON only."
    )
    text = generate_text(model, prompt, temperature=temperature, max_tokens=max_tokens)
    text = text.strip()
    if text.startswith("```"):  # best-effort strip fences
        text = text.strip("`")
        text = text.replace("json", "", 1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback: take first {...}
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start:end+1])
        raise OllamaError("Model did not return valid JSON")
