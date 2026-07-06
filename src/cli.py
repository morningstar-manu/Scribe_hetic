import sys
from datetime import date
from pathlib import Path

from src.config import OUTPUT_DIR
from src.summary import summarize
from src.transcription import transcribe


def run(audio_path: str) -> Path:
    """
    Pipeline complet : audio → transcription → compte rendu → fichier Markdown.

    Returns:
        Chemin du fichier Markdown généré.
    """
    print("Transcription en cours...")
    try:
        text = transcribe(audio_path)
    except FileNotFoundError as exc:
        print(f"Erreur : {exc}")
        sys.exit(1)
    except RuntimeError as exc:
        print(f"Erreur : {exc}")
        sys.exit(1)

    print("Rédaction du compte rendu...")
    try:
        report = summarize(text)
    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        print(f"Erreur : {exc}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    output_path = OUTPUT_DIR / f"compte-rendu_{today}.md"
    output_path.write_text(report, encoding="utf-8")

    print("\n" + "=" * 60)
    print(report)
    print("=" * 60)
    print(f"\nCompte rendu sauvegardé : {output_path}")

    return output_path


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage : python -m src.cli <chemin_fichier_audio>")
        sys.exit(1)

    run(sys.argv[1])


if __name__ == "__main__":
    main()