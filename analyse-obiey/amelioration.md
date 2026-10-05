# Propositions d'Améliorations - CyberCode Studio (DeepSeek-Coder V1)

Ce document présente une feuille de route détaillée des améliorations techniques, architecturales et opérationnelles proposées pour le projet **CyberCode Studio**, classées par catégorie.

---

## 1. Améliorations de la Sécurité & Moteur d'Audit (`serve/security_audit.py` & `serve/api_server.py`)

1. **Extension du Moteur Heuristique OWASP Top 10** :
   - Ajouter de nouvelles règles Regex pour détecter :
     - Injections SSRF (Server-Side Request Forgery).
     - Injections XXE (XML External Entity).
     - Desérialisation non sécurisée (`pickle.loads`, `yaml.unsafe_load`).
     - Configuration CORS permissive (`Access-Control-Allow-Origin: *`).
     - Cryptographie obsolète (DES, RC4, ECB mode dans AES).
2. **Analyse AST (Abstract Syntax Tree) Python & SAST Multi-Langage** :
   - Intégrer une analyse par arbre syntaxique (`ast` Python) en complément des Regex pour supprimer les faux positifs causés par les commentaires ou les chaînes littérales innocentes.
3. **Persistance Redis pour le Rate Limiting** :
   - Remplacer le dictionnaire en mémoire RAM (`rate_limit_store: dict`) de `api_server.py` par un magasin Redis ou sliding-window persistant afin de supporter le passage à l'échelle horizontal sur plusieurs répliques gérées par un load balancer.
4. **Gestion des Clés API Avancée** :
   - Implémenter un hachage des clés API (ex: SHA-256 avec sel) plutôt qu'une comparaison directe de chaînes en clair dans le code/environnement.

---

## 2. Améliorations de l'Inférence & API Server (`serve/`)

1. **Streaming des Réponses (Server-Sent Events / SSE)** :
   - Ajouter le support du mode `stream: true` dans `/v1/chat/completions` et `/v1/completions` en utilisant `StreamingResponse` de FastAPI / Starlette.
2. **Intégration Bounded Queue / Background Tasks pour les Audits Lourds** :
   - Déléguer les analyses de grands fichiers de code à une file d'attente asynchrone (Celery / FastAPI BackgroundTasks) avec retour d'un `job_id` et endpoint `/v1/security/audit/status/{job_id}`.
3. **OpenAPI / Swagger Enrichi & Métriques Prometheus** :
   - Exposer un point de terminaison `/metrics` pour Prometheus (temps de latence, nombre de requêtes par endpoint, taux d'erreurs 4xx/5xx, score moyen de sécurité).

---

## 3. Améliorations MLOps & Fine-Tuning (`finetune/`)

1. **Validation et Nettoyage de Données Accéléré** :
   - Optimiser `anonymize_code_and_text` dans `finetune_cybercode.py` en pré-compilant toutes les expressions régulières.
   - Ajouter la détection des clés privées RSA/SSH/PGP et des JWT tokens.
2. **Support de LoRA Target Modules Paramétrables** :
   - Permettre de cibler plus finement les couches d'attention et MLP (`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`) via la CLI.
3. **Integration MLflow / Weights & Biases (WandB)** :
   - Ajouter des flags d'activation pour le tracking automatique des métriques d'entraînement, de loss et d'évaluation vers WandB ou MLflow.

---

## 4. Améliorations DevOps, Conteneurisation & CI/CD

1. **Multi-Stage Build Docker Optimisé** :
   - Optimiser le `Dockerfile` avec un builder multi-stage pour réduire la taille de l'image de production et éliminer les dépendances de compilation inutiles dans le conteneur final.
2. **Healthchecks Docker Compose Avancés** :
   - Configurer des `healthcheck` rigoureux dans `docker-compose.yml` basés sur `/healthz` pour garantir le démarrage séquentiel des services dépendants.
3. **Sécurité Conteneur (Non-Root User)** :
   - Exécuter l'application dans le conteneur Docker sous un utilisateur non-privilégié (`appuser`, UID 10001) au lieu de `root`.

---

## 5. Améliorations des Tests Unitaires & Couverture (`tests/`)

1. **Mocking Amélioré des Appels Modèles** :
   - Permettre l'exécution fluide de toute la suite de tests sans nécessiter la présence physique de CUDA ou des poids de modèles lourds (via mocking PyTorch / HuggingFace Transformers).
2. **Fixtures Pytest Reutilisables** :
   - Refactoriser la suite de tests pour exploiter pleinement Pytest (fixtures `async_client`, fixtures d'authentification API).
3. **Calculateur de Couverture (Coverage Code)** :
   - Intégrer `pytest-cov` dans le workflow CI GitHub Actions avec un seuil minimal de couverture de code garanti à 85%+.
