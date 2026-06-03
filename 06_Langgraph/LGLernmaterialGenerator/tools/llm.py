"""LLM-Client, Token-Zähler und JSON-Extraktion.

Provider-agnostisch über die OpenAI-kompatible API (LM Studio / DeepInfra /
OpenRouter). ``call_llm`` ist die zentrale Aufruf-Funktion aller Graph-Knoten;
die Konfiguration reist im State mit, sodass die Knoten zustandslos bleiben.
Der Token-Zähler ist global ausgelegt (Einzelnutzer-Betrieb, eine Sitzung).
"""
import re
import json

from openai import OpenAI


# Globaler Token-Zähler. Wird zu Beginn jedes Laufs zurückgesetzt und in call_llm
# nach jeder Antwort fortgeschrieben. Ausgelegt für den Einzelnutzer-Betrieb (eine
# Gradio-Sitzung); bei echtem Mehrnutzer-Parallelbetrieb müsste man ihn pro Sitzung halten.
TOKENS = {"prompt": 0, "completion": 0, "total": 0, "calls": 0}

def reset_tokens():
    TOKENS.update(prompt=0, completion=0, total=0, calls=0)

def _add_usage(resp):
    u = getattr(resp, "usage", None)
    if not u:
        return  # manche Endpunkte liefern keine usage-Daten
    TOKENS["prompt"]     += getattr(u, "prompt_tokens", 0) or 0
    TOKENS["completion"] += getattr(u, "completion_tokens", 0) or 0
    TOKENS["total"]      += getattr(u, "total_tokens", 0) or 0
    TOKENS["calls"]      += 1


def call_llm(state: dict, system: str, user: str,
             temperature: float = 0.3, max_tokens: int = 4000,
             role: str = "generator") -> str:
    """Ein Chat-Completion-Aufruf gegen einen OpenAI-kompatiblen Endpunkt.

    role="checker" nutzt – falls gesetzt – ein eigenes Checker-Modell. Bleiben die
    Checker-Felder leer, wird automatisch das Generator-Modell verwendet. base_url und
    api_key des Checkers sind ebenfalls optional und fallen sonst auf die Generator-Werte
    zurück (so kann der Checker auch bei einem anderen Provider liegen).
    """
    if role == "checker" and state.get("checker_model"):
        base_url = (state.get("checker_base_url") or state["base_url"]).rstrip("/")
        api_key = state.get("checker_api_key") or state.get("api_key") or "not-needed"
        model = state["checker_model"]
    else:
        base_url = state["base_url"].rstrip("/")
        api_key = state.get("api_key") or "not-needed"   # LM Studio braucht keinen echten Key
        model = state["model"]
    client = OpenAI(base_url=base_url, api_key=api_key)
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    _add_usage(resp)
    return resp.choices[0].message.content or ""


def extract_json(text: str):
    """Holt das erste gültige JSON-Array/-Objekt aus einer Modellantwort."""
    t = text.strip()
    t = re.sub(r"^```(?:json)?", "", t).strip()
    t = re.sub(r"```$", "", t).strip()
    for opener, closer in (("[", "]"), ("{", "}")):
        start, end = t.find(opener), t.rfind(closer)
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(t[start:end + 1])
            except json.JSONDecodeError:
                continue
    raise ValueError("Konnte kein gültiges JSON aus der Modellantwort lesen.")
