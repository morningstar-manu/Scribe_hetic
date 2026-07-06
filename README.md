# Scribe_hetic

Scribe est un outil en ligne de commande qui transforme un enregistrement audio
(réunion, cours, note vocale) en compte rendu écrit et structuré.

## Fonctionnement

1. L'utilisateur fournit un fichier audio.
2. Un modèle Speech-to-Text (Groq) transcrit l'audio en texte brut.
3. Un LLM (Groq) reformule ce texte en compte rendu : titre, résumé, points clés, décisions/actions.

## Installation

```bash
python -m venv .venv
# Windows PowerShell :
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env   # puis renseigner GROQ_API_KEY
```

### Q2 — Choix des modèles

| Rôle | Modèle | Justification |
|------|--------|---------------|
| STT  | `whisper-large-v3-turbo` | Rapide, multilingue, moins cher que whisper-large-v3 ($0.04/h vs $0.111/h) |
| LLM  | `llama-3.3-70b-versatile` | Bon équilibre qualité / vitesse pour reformuler un texte structuré |



### Q3 — Que renvoie l'API STT en plus du texte ?

Avec `response_format="verbose_json"`, Groq renvoie notamment :
- la **langue détectée** (`language`)
- des **segments** avec horodatage (`start`, `end`, `text`)
- la **durée** de l'audio

Utile pour une évolution de Scribe : sous-titres, navigation par chapitres,
résumé par segment temporel, détection automatique de la langue.


### Q4 — Température

Température **0.2** (basse) : on veut un compte rendu fidèle à la transcription,
pas créatif. Une température élevée augmenterait le risque d'inventer des décisions
ou des actions absentes de l'audio.

### Q5 — Prompt système et tokens en cache

Le prompt système est renvoyé à chaque requête et consomme des tokens d'entrée.
Les providers peuvent mettre en cache les préfixes identiques (dont le system prompt)
pour réduire la latence et le coût sur les appels suivants — c'est le principe
du **prompt caching** vu en cours.