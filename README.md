# Test technique AI Engineer — Starter RAG

Bienvenue. Ce repo est le **point de départ** d'un test technique, pas un projet à utiliser tel quel.

👉 **Les consignes complètes, les livrables attendus et les critères d'évaluation sont dans [CONSIGNES.md](CONSIGNES.md). Commence par là.**

## Le scénario

Tu rejoins l'équipe AI Engineering. Un collègue a développé en quelques jours ce POC de chatbot RAG, qui répond aux questions des apprenants sur nos contenus de formation MLOps/LLMOps. Les supports sont dans `docs/`, ils sont ingérés au démarrage, et un endpoint `/ask` répond aux questions.

Ça tourne, et les réponses sont plutôt bonnes sur les questions simples. Mais ce n'est prêt ni pour la production, ni pour être mis devant des apprenants. **On te demande de le reprendre.**

Le code est volontairement livré en l'état, avec ses défauts. Une partie du travail consiste justement à les identifier — la liste ci-dessous n'est pas exhaustive.

## Ce qu'il y a dans le repo

| Fichier | Rôle |
|---|---|
| `app.py` | Toute la pipeline RAG : ingestion, chunking, embeddings, retrieval, génération, API |
| `docs/` | Les 4 contenus de formation servant de base de connaissances |
| `Dockerfile` | Build de l'image |
| `pyproject.toml` | Dépendances |
| `.env.example` | Template des variables d'environnement |
| `CONSIGNES.md` | **Le brief du test** |

## Faire tourner l'existant

Avant de modifier quoi que ce soit, vérifie que le POC démarre chez toi.

Avec Docker :

```bash
docker build -t formation-rag .
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... formation-rag
```

En local, avec [uv](https://docs.astral.sh/uv/) :

```bash
uv venv
uv pip install -r pyproject.toml
cp .env.example .env   # et mets ta clé dedans
uv run python app.py
```

Le serveur met une dizaine de secondes à démarrer, le temps de calculer les embeddings.

Puis :

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Pourquoi utiliser une image slim dans un Dockerfile ?"}'
```

Réponse attendue :

```json
{"answer": "..."}
```

### Variables d'environnement

| Variable | Obligatoire | Description |
|---|---|---|
| `OPENAI_API_KEY` | oui | Clé OpenAI, utilisée pour les embeddings et la génération |

Modèles utilisés : `text-embedding-3-small` pour les embeddings, `gpt-4o-mini` pour la génération. C'est en dur dans `app.py`.

Tu es libre de changer de provider (Mistral, Anthropic…) si tu préfères, tant que ça fonctionne — voir les contraintes dans `CONSIGNES.md`.

## Limitations connues du POC

Ce que le collègue avait lui-même noté avant de passer à autre chose :

- Aucun guardrail. Si on pose une question hors sujet, le modèle répond quand même, souvent n'importe quoi.
- Pas de gestion du « je ne sais pas ». Aucun score de confiance n'est renvoyé.
- Le vector store est en mémoire, donc reconstruit à chaque redémarrage. Ça coûte des appels d'embeddings à chaque fois.
- Chunking naïf à 500 caractères, sans overlap. Les phrases sont coupées en plein milieu.
- Pas de metadata sur les chunks : impossible de citer la source d'une réponse.
- Tout est dans `app.py`.
- Pas de tests, pas de logs structurés (que des `print`).
- Pas de `/health`, donc rien à brancher sur un load balancer.
- Le Dockerfile est le minimum syndical.

À toi de juger lesquels traiter en priorité, et de justifier tes arbitrages. Tu n'es pas censé tout corriger — voir le budget temps dans `CONSIGNES.md`.

## Rendu

Fork ce repo (ou crée un repo à partir de son contenu) et travaille sur ta copie. Les modalités de rendu sont détaillées dans [CONSIGNES.md](CONSIGNES.md).
