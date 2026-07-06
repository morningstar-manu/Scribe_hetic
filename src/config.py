import os
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

STT_MODEL = "whisper-large-v3-turbo"
LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.2  

PROMPT_PATH = PROJECT_ROOT / "prompts" / "system.txt"
OUTPUT_DIR = PROJECT_ROOT / "output"
SAMPLES_DIR = PROJECT_ROOT / "samples"


def get_api_key() -> str:
    """Retourne la clé API Groq ou quitte avec un message clair."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or not api_key.strip():
        print(
            "Erreur : la variable GROQ_API_KEY est absente.\n"
            "Créez un fichier .env à la racine du projet (voir .env.example)."
        )
        sys.exit(1)
    return api_key.strip()