from pathlib import Path

from groq import Groq
from groq import APIError, APIConnectionError, RateLimitError

from src.config import STT_MODEL, get_api_key


def transcribe(audio_path: str) -> str:
    """
    Transcrit un fichier audio en texte via l'API Groq Speech-to-Text.

    Args:
        audio_path: chemin vers le fichier audio (wav, mp3, m4a, etc.)

    Returns:
        Le texte transcrit.

    Raises:
        FileNotFoundError: si le fichier n'existe pas.
        RuntimeError: si l'API Groq renvoie une erreur.
    """
    path = Path(audio_path)

    if not path.exists():
        raise FileNotFoundError(f"Fichier audio introuvable : {path}")

    if not path.is_file():
        raise FileNotFoundError(f"Le chemin ne pointe pas vers un fichier : {path}")

    client = Groq(api_key=get_api_key())

    try:
        with path.open("rb") as audio_file:
            response = client.audio.transcriptions.create(
                file=audio_file,
                model=STT_MODEL,
                language="fr",    
                response_format="json", 
            )
    except FileNotFoundError:
        raise
    except (APIError, APIConnectionError, RateLimitError) as exc:
        raise RuntimeError(f"Erreur API Groq (transcription) : {exc}") from exc

    text = response.text if hasattr(response, "text") else str(response)
    return text.strip()