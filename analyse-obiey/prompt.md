# Prompt d'Implémentation des Améliorations - CyberCode Studio

> **Instructif** : Ce prompt est conçu pour être transmis à un agent IA ou un développeur afin d'implémenter de manière guidée, sécurisée et modulaire les améliorations proposées dans `analyse-obiey/amelioration.md`, tout en respectant l'architecture décrite dans `analyse-obiey/analyse.md`.

---

## Directives & Master Prompt

```markdown
Tu es un Ingénieur Expert en Cybersécurité, MLOps et Backend FastAPI Senior travaillant sur le projet **CyberCode Studio**.

### Contexte & Contraintes Absolues :
1. **Modèle Unique & Verrouillé** : Le projet repose EXCLUSIVEMENT sur les modèles **DeepSeek-Coder V1** (`1.3b-instruct`, `6.7b-instruct`, `33b-instruct`). Il est STRICTEMENT INTERDIT d'utiliser, d'importer ou de faire référence aux modèles DeepSeek V2, V3 ou R1. Les garde-fous existants (exceptions `ValueError` sur `v2`, `v3`, `r1`) doivent être rigoureusement maintenus.
2. **Rétrocompatibilité** : Toutes les fonctionnalités existantes (API OpenAI V1, fine-tuning LoRA, anonymisation RGPD, démo Gradio, scripts d'évaluation) doivent continuer à fonctionner sans régression.
3. **Qualité & Tests** : Chaque modification doit s'accompagner de tests unitaires ou d'intégration automatisés.

---

### Mission : Implémenter le Plan d'Amélioration Continu de CyberCode Studio

En t'inspirant des analyses fournies dans `analyse-obiey/analyse.md` et des propositions dans `analyse-obiey/amelioration.md`, réalise les étapes suivantes :

#### 1. Renforcement du Moteur d'Audit de Sécurité (`serve/security_audit.py`)
- Étends `SecurityAuditor` avec au moins 5 nouvelles règles Regex heuristiques OWASP :
  - SSRF (Server-Side Request Forgery)
  - XXE (XML External Entity)
  - Desérialisation non sécurisée (`pickle.loads`, `yaml.unsafe_load`)
  - En-têtes CORS permissifs (`Access-Control-Allow-Origin: *`)
  - Algorithmes cryptographiques obsolètes (DES, RC4, AES-ECB)
- Ajoute une méthode d'analyse statique syntaxique complémentaire basique basée sur le module standard `ast` de Python pour analyser les nœuds AST du code Python et réduire les faux positifs dans les commentaires.

#### 2. Modernisation & Fonctionnalités Avancées de l'API (`serve/api_server.py`)
- Ajoute le support du streaming (Server-Sent Events) dans `/v1/chat/completions` via `StreamingResponse` de FastAPI lorsque `stream=True` est demandé.
- Améliore le module d'anonymisation des logs pour masquer également les jetons JWT et les blocs de clés privées.
- Expose un point de terminaison `/metrics` exposant des métriques JSON/Prometheus basiques (compteur de requêtes, temps moyen d'exécution, score moyen de sécurité).

#### 3. Perfectionnement du Pipeline de Fine-Tuning RGPD (`finetune/finetune_cybercode.py`)
- Pré-compile les expressions régulières d'anonymisation pour accélérer le traitement des jeux de données volumineux.
- Ajoute le masquage automatique des blocs de clés RSA/SSH (`-----BEGIN PRIVATE KEY-----`) et des jetons JWT.

#### 4. Optimisation Docker & DevOps (`Dockerfile`, `docker-compose.yml`)
- Mets à jour le `Dockerfile` pour exécuter l'application sous un utilisateur non-root (`USER 10001`).
- Ajoute des blocs `healthcheck` valides dans `docker-compose.yml` basés sur `curl -f http://localhost:8000/healthz`.

#### 5. Validation par les Tests (`tests/`)
- Mets à jour ou ajoute des tests unitaires dans `tests/test_security_audit.py` et `tests/test_api_security.py` pour valider :
  - Les nouvelles règles de vulnérabilités (SSRF, XXE, Deserialization, etc.).
  - L'anonymisation étendue des clés privées et JWT.
  - Le fonctionnement du point de terminaison `/metrics`.
- Exécute toute la suite de tests (`python3 -m unittest discover tests`) et confirme qu'il n'y a aucune régression.
```
