# TODO — Test technique AI Engineer

## 0. Cadrage
- [x] Vérifier que le POC original (`app.py`) démarre.
- [x] `.gitignore` / `.dockerignore` à jour (`.env`, `.venv`, `__pycache__`, index vectoriel local).

## 1. Architecture (`app/`)
- [x] `main.py` : instancier FastAPI, monter le router.
- [x] `config.py` : centraliser les paramètres (modèles, chemins, taille de chunk, top_k, seuil...).
- [x] `schemas.py` : requêtes/réponses Pydantic.
- [x] `api/routes.py` : uniquement l'orchestration HTTP.
- [x] `services/ingestion.py`, `retrieval.py`, `generation.py` : logique métier.
- [x] Décider quoi faire de l'ancien `app.py` (garder en compat, ou supprimer).

## 2. Ingestion
- [x] Multi-format (`.md`, `.txt`, `.pdf`).
- [x] Validation des entrées + gestion d'erreur (fichier vide, illisible, dossier absent).
- [x] Métadonnées utiles par chunk.
- [x] Stratégie de chunking — **Langchain**

## 3. Retrieval + guardrail + génération
- [x] Retrieval : top_k, scores, métadonnées.
- [x] Guardrail — **Seuil=0.9** (voir tableau d'options dans `CONSIGNES.md`).
- [x] Génération : prompt contraint au contexte, gestion du "je ne sais pas", sources citées.

## 4. API + observabilité
- [x] `GET /health`.
- [x] Validation des entrées de `/query`, codes HTTP cohérents.
- [x] Logs structurés — décider quoi logger et où.

## 5. Tests (au moins 2, pytest)
- [x] Identifier les 2 comportements les plus importants à couvrir sans coût API.
- [x] Mocker ce qui appelle OpenAI/Chroma.

## 6. Dockerfile
- [x] Au moins 3 améliorations, chacune justifiable à l'oral.
- [x] Vérifier `docker build` + `docker run` + `/health` après coup.

## 7. README
- [x] Architecture et rôle de chaque module.
- [x] Installation (local + Docker).
- [x] Section **Arbitrages** : ce que j'ai choisi, ce que j'ai écarté, ce que je n'ai pas eu le temps de faire.
