# Assistant RAG — Contenus de formation

Chatbot RAG qui répond aux questions des apprenants à partir des contenus de
formation LLMOps/MLOps (`docs/`). Reprise et industrialisation d'un POC
initial : architecture modulaire, ingestion multi-format, guardrail de
pertinence, observabilité minimale, tests, et exécution via Docker.

## Ce qu'il y a dans le repo

| Fichier / dossier | Rôle |
|---|---|
| `app/main.py` | Point d'entrée FastAPI, monte le router |
| `app/config.py` | Configuration centralisée (Pydantic Settings), modes `openai`/`ollama` |
| `app/schemas.py` | Schémas de requête/réponse de l'API |
| `app/api/routes.py` | Endpoints `POST /query` et `GET /health` |
| `app/services/ingestion.py` | Chargement multi-format, validation, chunking, embeddings, stockage Chroma |
| `app/services/retrieval.py` | Recherche vectorielle + guardrail sur le score de pertinence |
| `app/services/generation.py` | Construction du prompt et appel au LLM |
| `docs/` | Les contenus de formation servant de base de connaissances |
| `test/` | Tests pytest (validation ingestion, guardrail) |
| `Dockerfile` | Build de l'image |
| `pyproject.toml` | Dépendances |
| `.env.example` | Template des variables d'environnement |

## Faire tourner le projet

### Mode `ollama` (local, sans coût)

Nécessite Ollama lancé en local, avec les modèles `qwen3-embedding` et
`gemma4` déjà tirés (`ollama pull ...`).

```bash
docker build -t formation-rag .
docker run --network=host --env-file .env formation-rag
```

`--network=host` est nécessaire car Ollama n'écoute que sur `127.0.0.1` — un
conteneur ne peut pas l'atteindre autrement. Commande spécifique à Linux (pas
disponible tel quel sur Docker Desktop Mac/Windows).

### Mode `openai` (avec une clé API payante)

Renseigner `LLM_PROVIDER=openai` et la clé API dans `OPENAI_API_KEY` (`.env`), puis :

```bash
docker build -t formation-rag .
docker run -p 8000:8000 --env-file .env formation-rag
```

Pas besoin de `--network=host` ici, puisqu'il n'y a pas d'appel à un service
local — seulement des appels sortants vers l'API OpenAI.

> ⚠️ **Le seuil du guardrail (0.9) est calibré sur les scores obtenus avec
> les embeddings Ollama, pas avec OpenAI.** Les deux modèles produisent des
> espaces vectoriels différents, donc des échelles de score différentes (un
> score de 0.68 a été observé avec OpenAI sur une question en-sujet — à
> comparer à 0.43-0.73 avec Ollama). En mode `openai`, le guardrail peut donc
> se déclencher de façon moins fiable tant que ce seuil n'a pas été
> recalibré spécifiquement pour ce provider — voir la section Arbitrages.

En local, avec [uv](https://docs.astral.sh/uv/) :

```bash
uv sync
cp .env.example .env   # renseigne les variables selon le mode choisi
uv run uvicorn app.main:app --reload
```

Le serveur met quelques secondes à démarrer, le temps de calculer les embeddings.

Puis :

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "À quoi sert Docker ?"}'
```

Réponse attendue :

```json
{"answer": "...", "sources": ["docs/01_introduction_docker.md"], "context_found": true}
```

### Variables d'environnement

| Variable | Obligatoire | Description |
|---|---|---|
| `LLM_PROVIDER` | oui | `openai` ou `ollama` |
| `OPENAI_API_KEY` | si `LLM_PROVIDER=openai` | Clé OpenAI |
| `EMBEDDING_MODEL` / `CHAT_MODEL` | si `LLM_PROVIDER=openai` | Modèles OpenAI |
| `OLLAMA_BASE_URL` | si `LLM_PROVIDER=ollama` | ex: `http://localhost:11434` |
| `EMBEDDING_MODEL_LOCAL` / `CHAT_MODEL_LOCAL` | si `LLM_PROVIDER=ollama` | Modèles Ollama |
| `DOCS_DIR` | oui | Dossier des documents à ingérer |
| `CHROMA_DIR` | oui | Dossier de persistance de l'index vectoriel |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | oui | Paramètres de découpage |
| `TOP_K` | oui | Nombre de chunks récupérés par requête |
| `SYSTEM_PROMPT` | oui | Instruction système du LLM |

## État par rapport au POC original

Le POC de départ (`app.py`, supprimé depuis) n'avait aucun guardrail, un
chunking naïf à 500 caractères sans overlap, aucune métadonnée sur les
chunks, aucun test, pas de `/health`, et un Dockerfile minimal. Le détail de
ce qui a été traité, comment, et ce qui a été volontairement laissé de côté
est dans la section **Arbitrages** ci-dessous.

# Arbitrages

Sur le créneau de 8 à 10h, j'ai priorisé trois axes, dans cet ordre :

1. **Fiabiliser l'ingestion** — le POC initial ne gérait que le Markdown avec
   un découpage fixe. J'ai ajouté le support des fichiers texte et PDF, un
   chunking avec chevauchement, la conservation des métadonnées, et la
   gestion des documents vides.
2. **Rendre le RAG réellement exécutable et indépendant d'un fournisseur
   unique** — séparation de la configuration OpenAI/Ollama, avec Ollama pour
   pouvoir tester localement toute la chaîne (embeddings, indexation Chroma,
   retrieval, génération) sans coût.
3. **Fiabiliser la réponse** — seuil de pertinence pour éviter d'interroger
   inutilement le LLM, restitution des sources, logs sur les étapes
   importantes, et des tests unitaires ciblés sur les comportements les plus
   critiques.

L'objectif sur ce créneau n'était donc pas de construire une plateforme
complète, mais de sécuriser le chemin critique du POC et de rendre les
principaux choix techniques explicites et testables. Volontairement laissés
de côté : CI/CD, dashboard d'observabilité, couverture de tests élevée,
rechargement incrémental de l'index, gestion des formats non supportés et de
la limitation de taille des fichiers (détails par section ci-dessous).

## Provider LLM (OpenAI / Ollama)

Dépendance à une clé API payante : réalisation des embeddings en local avec
`qwen3-embedding`, à la place de `text-embedding-3-small`, et `gemma4` à la
place de `gpt-4o-mini`. Ces changements permettent d'avoir quelque chose de
comparable au POC initial sans coût.

## Configuration (`config.py`)

Les variables étaient codées en dur dans l'ancien POC. Amélioration réalisée
dans `config.py`, en lien avec les variables d'environnement du `.env`
(`DOCS_DIR`, `CHUNK_SIZE`, `TOP_K`, `EMBEDDING_MODEL`, `CHAT_MODEL`,
`SYSTEM_PROMPT`, etc.) : vérification de chaque variable d'environnement et
gestion propre, sans valeurs codées en dur.

## Schémas (`schemas.py`)

Question limitée à 2000 caractères pour éviter les requêtes démesurées.
`str_strip_whitespace` retire les espaces en début/fin de chaîne, ce qui
évite les questions composées uniquement d'espaces.

## Ingestion (`ingestion.py`)

Choix de `langchain`/`langchain-community` : ils fournissent des outils de
split déjà en place, c'est le choix le plus courant. Le splitter tranche sur
les frontières naturelles dans un ordre de préférence (`\n\n`, puis `\n`,
etc.) au lieu de trancher au caractère 500 sans regarder ce qu'il y a
autour — un défaut de l'ancien code.

Pour les chunks : 500 caractères avec un overlap de 100. Les documents dans
`docs/` ont des paragraphes entre 315 et 448 caractères, donc 500 les
contient sans les couper la plupart du temps.

Non traité, faute de temps : les formats non supportés (`.docx`, etc.), la
limitation de taille des fichiers.

## Stockage vectoriel (Chroma)

Chroma avec dossier persistant. L'index est recalculé à chaque démarrage
(pas de rechargement incrémental) — accepté pour tenir le budget de temps.

## Guardrail (`retrieval.py`)

J'ai choisi un seuil de similarité plutôt qu'un framework dédié (NeMo
Guardrails, Guardrails AI, LLM Guard...) parce que c'était la méthode la
plus rapide à mettre en œuvre et la plus simple à comprendre et à
expliquer. Comme le rappelle Sébastien dans son email : « Un périmètre
restreint mais assumé et documenté vaut mieux qu'un rendu large et
superficiel. [...] on apprécie la transparence et la capacité à identifier
ce qu'on ne maîtrise pas encore. » Je n'ai pas eu le temps d'évaluer ces
frameworks et je l'assume : je ne les maîtrise pas encore, et un seuil sur
le score de retrieval reste une solution simple, explicable, et suffisante
pour ce périmètre.

Après avoir réalisé des tests avec un retrieval basique, j'ai remarqué que
les scores oscillaient entre 0.43 et 0.73 lorsque la question était en
sujet, et autour de 1.31 lorsqu'elle était hors sujet (questions aléatoires
sans rapport avec les documents). J'ai donc fixé un seuil à 0.9, une valeur
intermédiaire entre les deux groupes observés : au-delà, la question est
considérée trop éloignée du contexte disponible pour qu'on y réponde.

Le seuil est calibré pour le mode Ollama et non re-testé pour OpenAI, dont
l'échelle de score est différente (0.68 observé en test, à comparer à un
autre seuil que celui d'Ollama).

Je ne connaissais pas la distinction entre score de similarité et score de
distance en recherche vectorielle avant ce test — j'ai vérifié empiriquement
sur mes propres données plutôt que de supposer, ce qui m'a évité d'inverser
le sens de comparaison du guardrail.

## Dockerfile

Trois améliorations, chacune simple et justifiable à l'oral :
- Utiliser une image Python plus légère (`slim`), pour une construction et
  un téléchargement plus rapides.
- Copier `pyproject.toml` avant le reste du code pour tirer parti du cache
  Docker : les dépendances ne sont réinstallées que si ce fichier change.
- Désactiver le cache lors de l'installation avec pip et uv, pour ne pas
  alourdir l'image avec des fichiers temporaires.

Lors de l'exécution avec Ollama, il faut utiliser `--network=host` : le
réseau du conteneur doit être partagé avec celui de la machine hôte pour
pouvoir accéder à Ollama, qui n'écoute que sur `localhost` et n'est donc pas
joignable autrement depuis un conteneur.

## Tests (`test/`)

Deux comportements critiques du pipeline sont couverts. `test_guardrail.py`
vérifie que le guardrail rejette une question avec un score faible (sans
jamais appeler le LLM) et accepte une question avec un bon score.
`test_ingestion.py` vérifie qu'un document au contenu vide est rejeté avant
d'entrer dans Chroma, et qu'un document valide est conservé.

J'ai privilégié ces deux zones plutôt que `/health` (trop simple, apporte
peu de valeur fonctionnelle) parce que la qualité du RAG dépend directement
de la qualité des documents indexés, et parce que le guardrail détermine si
le système doit répondre ou reconnaître qu'il ne dispose pas d'un contexte
suffisamment pertinent — ce sont les règles métier les plus importantes, et
les plus faciles à tester de façon isolée avec le temps disponible.

## Observabilité

Logs `logging` standard plutôt que du JSON structuré ou une intégration
Langfuse/Phoenix : ça répond au besoin principal du POC — disposer
rapidement de logs lisibles pour suivre le chargement des documents, les
fichiers ignorés et les erreurs — sans ajouter de dépendance ni de service
externe.
