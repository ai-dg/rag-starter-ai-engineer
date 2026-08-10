# Test technique — AI Engineer

## Contexte

Tu rejoins l'équipe AI Engineering. Un collègue a développé ce POC de chatbot RAG en quelques jours pour répondre aux questions des apprenants sur nos contenus de formation. Il fonctionne, mais il n'est prêt ni pour la production, ni pour être présenté à des apprenants.

On te demande de le reprendre.

## Ce qu'on te demande

### Livrable 1 — Code (repo GitHub)

- **Réorganiser le projet** en architecture propre, avec une séparation claire des responsabilités : ingestion, retrieval, génération, API.
- **Améliorer la pipeline d'ingestion** : gestion multi-format, validation des entrées, gestion d'erreur, et une stratégie de chunking argumentée.
- **Implémenter au moins un guardrail** : détection de question hors-contexte, score de confiance, gestion du « je ne sais pas »… Le choix t'appartient, mais justifie-le. Quelques pistes non exhaustives, à titre de suggestions :

  | Outil | Ce que ça couvre |
  |---|---|
  | [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) (NVIDIA) | Rails conversationnels déclaratifs (Colang) : cadrage du sujet, refus, vérification de la réponse |
  | [Guardrails AI](https://github.com/guardrails-ai/guardrails) | Validateurs composables sur la sortie (format, toxicité, hallucination) avec re-ask automatique |
  | [LLM Guard](https://github.com/protectai/llm-guard) | Scanners entrée/sortie : prompt injection, données sensibles, toxicité |
  | [Presidio](https://github.com/microsoft/presidio) (Microsoft) | Détection et anonymisation de PII |
  | [Ragas](https://github.com/explodinggradients/ragas) / [DeepEval](https://github.com/confident-ai/deepeval) | Scoring de faithfulness / relevance, utilisable comme garde-fou en ligne ou en test |

  Une implémentation maison est parfaitement acceptable — un seuil sur le score de similarité du retrieval, ou un LLM-as-a-judge minimal, peuvent suffire. **On évalue la pertinence du choix et la qualité de l'implémentation, pas le nombre de librairies.** Une solution simple et bien argumentée vaut mieux qu'un framework lourd mal intégré.
- **Ajouter un minimum d'observabilité** : logs structurés, métriques basiques, ou une intégration légère type Langfuse / Phoenix. Pas besoin d'un dashboard complet.
- **Revoir le Dockerfile** : au moins 3 améliorations, argumentées.
- **Ajouter au moins 2 tests** (pytest).
- **Un README clair** expliquant tes choix d'architecture, comment lancer le projet, et les améliorations apportées.

### Livrable 2 — Slides (5 à 10 slides)

Une présentation du concept **« Guardrails et observabilité pour un pipeline RAG en production »**, destinée à un public débutant (apprenants en formation).

Le support doit être compréhensible par quelqu'un qui sait ce qu'est un RAG mais qui n'en a jamais mis un en production.

### Livrable 3 — Vidéo (5 à 7 minutes max)

Une présentation orale de tes slides, comme si tu animais une masterclass devant un groupe d'apprenants débutants.

Captation simple (Loom, Zoom, ou autre). Aucun montage attendu.

## Contraintes

- **Délai** : 1 semaine à compter de la réception.
- Tu peux utiliser n'importe quel framework ou librairie, tant que tu justifies ton choix.
- Le code doit tourner avec `docker compose up`, ou a minima `docker build` + `docker run`.
- Tu peux changer de LLM provider si tu préfères (Mistral, Anthropic, etc.), tant que ça fonctionne.
- **Ne passe pas plus de 8 à 10h au total** sur l'ensemble. On évalue ta capacité à prioriser, pas à tout faire.

## Ce qu'on évalue

- La qualité de la réorganisation et la justification des choix d'architecture.
- La pertinence du guardrail choisi et la qualité de son implémentation.
- La rigueur d'engineering : Docker, tests, logs, gestion d'erreur.
- La clarté pédagogique des slides et de la vidéo.
- La capacité à vulgariser pour un public non-expert.
- Le README et la documentation du code.

## Ce qui ferait échouer le test

- Du code qui ne tourne pas.
- Aucun guardrail implémenté malgré la consigne.
- Des slides incompréhensibles pour un débutant.
- Une vidéo qui récite un script, sans capacité à expliquer.
- L'absence totale de tests ou de logging.

## Ce qui n'est PAS attendu

- Un système de monitoring complet avec dashboard.
- Du fine-tuning ou du training.
- Une UI frontend.
- Une couverture de tests à 100 %.
- Un système multi-agents.

## Rendu

Envoie-nous le lien du repo GitHub, les slides (PDF ou lien), et le lien de la vidéo.
