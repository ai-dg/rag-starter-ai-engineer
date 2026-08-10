# TODO — Test technique AI Engineer

## 0. Cadrage
- [x] Vérifier que le POC original (`app.py`) démarre.
- [x] `.gitignore` / `.dockerignore` à jour (`.env`, `.venv`, `__pycache__`, index vectoriel local).

## 1. Architecture (`app/`)
- [ ] `main.py` : instancier FastAPI, monter le router.
- [x] `config.py` : centraliser les paramètres (modèles, chemins, taille de chunk, top_k, seuil...).
- [x] `schemas.py` : requêtes/réponses Pydantic.
- [ ] `api/routes.py` : uniquement l'orchestration HTTP.
- [ ] `services/ingestion.py`, `retrieval.py`, `generation.py` : logique métier.
- [ ] Décider quoi faire de l'ancien `app.py` (garder en compat, ou supprimer).

## 2. Ingestion
- [ ] Multi-format (`.md`, `.txt`, `.pdf`).
- [ ] Validation des entrées + gestion d'erreur (fichier vide, illisible, dossier absent).
- [ ] Métadonnées utiles par chunk.
- [ ] Stratégie de chunking — **à choisir**

## 3. Retrieval + guardrail + génération
- [ ] Retrieval : top_k, scores, métadonnées.
- [ ] Guardrail — **choix à faire et à justifier** (voir tableau d'options dans `CONSIGNES.md`).
- [ ] Génération : prompt contraint au contexte, gestion du "je ne sais pas", sources citées.

## 4. API + observabilité
- [ ] `GET /health`.
- [ ] Validation des entrées de `/ask`, codes HTTP cohérents.
- [ ] Logs structurés — décider quoi logger et où.

## 5. Tests (au moins 2, pytest)
- [ ] Identifier les 2 comportements les plus importants à couvrir sans coût API.
- [ ] Mocker ce qui appelle OpenAI/Chroma.

## 6. Dockerfile
- [ ] Au moins 3 améliorations, chacune justifiable à l'oral.
- [ ] Vérifier `docker build` + `docker run` + `/health` après coup.

## 7. README
- [ ] Architecture et rôle de chaque module.
- [ ] Installation (local + Docker).
- [ ] Section **Arbitrages** : ce que j'ai choisi, ce que j'ai écarté, ce que je n'ai pas eu le temps de faire.

## 8. Slides + vidéo
- [ ] 5-10 slides, public débutant : "Guardrails et observabilité pour un RAG en prod".
- [ ] Vidéo 5-7 min, script écrit, répétée avant enregistrement.

## Point d'arrêt minimal (ne pas dépasser sans que ça marche)
- [ ] `docker compose up` (ou build+run) fonctionne.
- [ ] Une question dans le sujet répond correctement.
- [ ] Une question hors sujet déclenche le guardrail.
- [ ] Les tests passent.
- [ ] Le README explique mes choix.
