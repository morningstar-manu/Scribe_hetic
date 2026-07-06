from groq import Groq
from groq import APIError, APIConnectionError, RateLimitError

from src.config import (
    LLM_MODEL,
    LLM_TEMPERATURE,
    PROMPT_PATH,
    get_api_key,
)


def _load_system_prompt() -> str:
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(
            f"Prompt système introuvable : {PROMPT_PATH}"
        )
    return PROMPT_PATH.read_text(encoding="utf-8").strip()


def summarize(transcript: str) -> str:
    """
    Transforme une transcription brute en compte rendu structuré via Groq LLM.

    Args:
        transcript: texte brut issu de la transcription audio.

    Returns:
        Compte rendu au format Markdown.
    """
    if not transcript or not transcript.strip():
        raise ValueError("La transcription est vide.")

    system_prompt = _load_system_prompt()
    client = Groq(api_key=get_api_key())

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        "Voici la transcription à transformer en compte rendu :\n\n"
                        f"{transcript.strip()}"
                    ),
                },
            ],
        )
    except (APIError, APIConnectionError, RateLimitError) as exc:
        raise RuntimeError(f"Erreur API Groq (compte rendu) : {exc}") from exc

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Le LLM n'a renvoyé aucun contenu.")

    return content.strip()