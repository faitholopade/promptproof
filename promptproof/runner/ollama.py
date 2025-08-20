from __future__ import annotations
import httpx
import json

OLLAMA_URL = "http://localhost:11434"

class OllamaError(RuntimeError):
    pass

def _post_json(path: str, payload: dict) -> dict:
    url = f"{OLLAMA_URL}{path}"
    try:
        with httpx.Client(timeout=120) as c:
            r = c.post(url, json=payload)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise OllamaError(f"Ollama request failed: {e}")

def generate_text(model: str, prompt: str, temperature: float = 0.2, max_tokens: int = 512) -> str:
    """
    Simple wrapper for /api/generate. Non-streaming for simplicity.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "options": {"temperature": temperature, "num_predict": max_tokens}
    }
    data = _post_json("/api/generate", payload)
    return data.get("response", "")

def generate_json(model: str, system: str, user: str, schema_hint: str, temperature: float = 0.2, max_tokens: int = 512) -> dict:
    """
    Coax JSON by hard-instructing the format. We do one best-effort parse.
    """
    prompt = (
        f"{system}\n\n"
        f"{user}\n\n"
        "Respond ONLY as strict JSON that validates against this schema concept:\n"
        f"{schema_hint}\n"
        "Do not include explanations, markdown, or extra text."
    )
    text = generate_text(model, prompt, temperature=temperature, max_tokens=max_tokens)
    # Best-effort strip code fences if any
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback: attempt to find first {...} block
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            frag = text[start:end+1]
            return json.loads(frag)
        raise OllamaError("Model did not return valid JSON")
