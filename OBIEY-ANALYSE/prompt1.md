# CAHIER DES CHARGES DÉTAILLÉ ET STRUCTURÉ – VERSION PERSONNALISÉE DEEPSEEK-CODER POUR CYBERCODE STUDIO

![CyberCode Studio](../cybercode-couverture-linkedin-1584x396.png)

> **Directive principale** : Ce document guide la modernisation, la sécurisation et l’extension du projet DeepSeek-Coder V1, afin d’en faire une **solution personnalisée sur mesure pour CyberCode Studio**. Toutes les fonctionnalités existantes (scripts d’évaluation, fine-tuning DeepSpeed ZeRO-3, démo Gradio) doivent être **rigoureusement préservées et rester rétrocompatibles**. **Aucune migration vers DeepSeek-Coder-V2, V3 ou R1 n’est autorisée.**

---

## 1. CONTEXTE, VISION ET DISTINCTION ORIGINAL VS PERSONNALISÉ

### 1.1 Context et Ambition
Le projet d'origine fournit la baseline officielle de **DeepSeek-Coder V1**. Bien que fonctionnel pour la recherche et la démonstration, le code de base nécessite une mise au niveau industrielle moderne (2024-2025). CyberCode Studio transforme ce projet en un service d'intelligence artificielle souverain, sécurisé et spécialisé pour l'ingénierie logicielle et la cybersécurité.

### 1.2 Clarification : Code Original vs Personnalisation CyberCode Studio

| Élément | Baseline Originale (DeepSeek-AI) | Extensions Personnalisées CyberCode Studio |
| :--- | :--- | :--- |
| **Poids et Modèle** | Baseline DeepSeek-Coder V1 (1.3B, 6.7B, 33B) | Conservation stricte des poids V1 avec adaptateurs LoRA/QLoRA métier |
| **Inférence / Serveur API** | Démo Gradio (`demo/app.py`), scripts CLI | API FastAPI/vLLM compatible OpenAI (`serve/api_server.py`, `vllm_server.py`) |
| **Fine-Tuning** | Full SFT via DeepSpeed ZeRO-3 uniquement | Support PEFT (LoRA/QLoRA 4-bit/8-bit), script de fusion, pipeline continu |
| **Cybersécurité** | Aucune fonctionnalité native d'audit | Engine d'audit (`serve/security_audit.py`), revue PR automatisée, OWASP Top 10 |
| **Conteneurisation & CI/CD** | Absent | Dockerfile, docker-compose multi-services, GitHub Actions CI/CD avec scans security |
| **Sécurité & Conformité** | Absente | Auth Bearer JWT/API Key, HashiCorp Vault, TLS 1.3, anonymisation RGPD, SBOM |
| **Tests & Qualité** | Harnais d'évaluation benchmarks uniquement | Suite `pytest`, linters `ruff`/`black`/`mypy`, tests de charge Locust, Trivy, Bandit |

---

## 2. RÈGLES ET CONTRAINTES STRICTES

1. **Conservation du code existant** : Ne supprime aucun fichier ni aucun comportement existant. Toutes les améliorations doivent être apportées par refactorisation non-cassante ou par ajout de nouvelles options/modules.
2. **Compatibilité descendante** : Les commandes et scripts du `README.md` original doivent continuer de fonctionner à 100 %.
3. **Verrouillage absolu sur la V1** : Utiliser exclusivement les poids DeepSeek-Coder V1 (`deepseek-ai/deepseek-coder-1.3b-instruct`, `deepseek-ai/deepseek-coder-6.7b-instruct`, `deepseek-ai/deepseek-coder-33b-instruct`). Interdiction formelle de télécharger ou référencer toute version ultérieure (V2, V3, R1).
4. **Non-régression** : Toute mise à jour de dépendance doit être validée par des tests sur les poids V1.
5. **Modularité et réutilisabilité** : Code typé (type hints), docstrings, gestion d’exceptions explicite, briques autonomes.
6. **Canaux de communication** : Remplacement de tous les liens obsolètes ou non pertinents (Discord baseline, WeChat) par les canaux officiels de CyberCode Studio (LinkedIn, WhatsApp Business, Email direct, GitHub Discussions).

---

## 3. PRÉREQUIS MATÉRIELS ET CONFIGURATION MINIMALE

### 3.1 Exigences Matérielles (RAM / VRAM)

| Environnement | Profil | RAM Système Min. | VRAM GPU Min. | GPU Recommandé | Stockage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Développement Local** | Modèle 1.3B / 6.7B (QLoRA 4-bit) | 16 Go | 8 Go | RTX 3060 / RTX 4060 / Apple M-Series | 50 Go SSD NVMe |
| **Inférence Dev / Test** | Modèle 6.7B FP16 | 32 Go | 16 Go | RTX 4080 / RTX 4090 / T4 | 100 Go SSD NVMe |
| **Production Serveur** | Modèle 6.7B / 33B (vLLM / FP16) | 64 Go | 24 Go à 80 Go | NVIDIA A10G / A100 / H100 | 200 Go SSD NVMe |
| **Fine-Tuning Full SFT** | Modèle 6.7B / 33B (ZeRO-3) | 128 Go | 4 x 80 Go | Cluster 4x A100 (80 Go) | 500 Go SSD NVMe |

---

## 4. DÉMARRAGE RAPIDE & QUICKSTART DOCKER

### 4.1 Quickstart Docker (API fonctionnelle en 5 minutes)

Lancer l'API sécurisée compatible OpenAI et la démo Web CyberCode Studio avec Docker en 5 minutes :

```bash
# 1. Cloner le dépôt et se positionner
git clone https://github.com/CyberCode-Studio/deepseek-coder-cybercode.git
cd deepseek-coder-cybercode

# 2. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env pour définir VOTRE_CLE_API_SECRETE et la configuration TLS

# 3. Lancer la pile complète via Docker Compose
docker-compose up -d --build

# 4. Vérifier l'état des services
docker-compose ps

# 5. Tester le point de terminaison d'audit de sécurité
curl -X POST http://localhost:8000/v1/security/audit \
  -H "Authorization: Bearer VOTRE_CLE_API_SECRETE" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "SELECT * FROM users WHERE username = '\''" + input_user + "'\'';",
    "langage": "python"
  }'
```

---

## 5. ARCHITECTURE ET SÉCURITÉ DE L'API

### 5.1 Sécurité de l'API & Gestion des Accès
- **Authentification & Autorisation** : Authentification par jetons API Bearer (`Authorization: Bearer <token>`) vérifiée via des middlewares FastAPI stricts.
- **Rate Limiting** : Limitation du nombre de requêtes par minute (ex. 100 req/min par clé client) avec retour HTTP 429 Too Many Requests.
- **Gestion des secrets via Vault** : Intégration native avec **HashiCorp Vault** (ou AWS Secrets Manager) pour l'injection sécurisée des clés d'API, certificats TLS et clés de chiffrement au démarrage. Aucune clé en clair dans le code.
- **Chiffrement TLS 1.3** : Communication chiffrée de bout en bout en transit via HTTPS/TLS 1.3 géré par reverse-proxy Nginx ou Traefik avec renouvellement automatique Let's Encrypt.
- **Chiffrement des données au repos** : Chiffrement AES-256 pour les jeux de données, adaptateurs LoRA et journaux d'audit.

### 5.2 Endpoints Inférence et Cybersécurité
- `POST /v1/chat/completions` : Inférence conversationnelle compatible OpenAI.
- `POST /v1/completions` : Complétion de code et support FIM (`<｜fim begin｜>`, `<｜fim hole｜>`, `<｜fim end｜>`).
- `POST /v1/security/audit` : Audit de sécurité de code source avec rapport JSON structuré.
- `POST /v1/code/review` : Revue automatisée de PR et détection des failles.
- `POST /v1/code/generate` : Génération de code sécurisé conforme aux standards OWASP Top 10.
- `GET /v1/models` : Liste des modèles V1 disponibles.
- `GET /healthz` : Healthcheck pour orchestrateurs et load balancers.

---

## 6. TESTS, ASSURANCE QUALITÉ ET CI/CD

### 6.1 Stratégie de Tests & CI/CD
- **pytest** : Tests unitaires et d'intégration couvrant le tokenizer FIM, les templates de chat, les endpoints FastAPI, le module d'audit et le fine-tuning LoRA.
- **ruff & black & mypy** : Validation automatique du style de code, du formatage et du typage statique.
- **GitHub Actions** : Workflow automatisé `.github/workflows/ci.yml` déclenché à chaque commit et Pull Request pour exécuter :
  1. Linting et contrôle de typage (`ruff`, `mypy`).
  2. Tests unitaires et de non-régression (`pytest`).
  3. Scan d'analyse statique de sécurité (`bandit`).
  4. Scan de vulnérabilités d'image Docker (`trivy`).

### 6.2 Automation de Sécurité & Performance
- **Locust** : Scripts de test de charge simulant 100, 500 et 1000 utilisateurs simultanés pour valider la latence (TTFT < 300 ms) et vérifier l'absence d'erreurs d'allocation mémoire.
- **Bandit** : Scan de sécurité statique du code Python.
- **Trivy** : Inspection continue des conteneurs Docker pour identifier les CVEs.
- **Dependabot** : Mises à jour automatisées des dépendances avec alertes de sécurité.
- **.pre-commit-config.yaml** : Hooks git locaux exécutant `ruff`, `black` et `mypy` avant chaque validation.
- **Tests de non-régression** : Validation automatique sur un jeu de référence pour garantir la conservation des performances et de l'exactitude des complétions V1.

---

## 7. DÉPLOIEMENT VPS ET INFRASTRUCTURE DE PRODUCTION

### 7.1 Architecture Déploiement VPS
- **Conteneurisation multi-services** : Fichier `docker-compose.prod.yml` prêt pour la production avec redémarrage automatique (`restart: always`), limites de ressources RAM/CPU/GPU et rotation des journaux (`json-file`).
- **Reverse Proxy Nginx / Traefik** : Interception du trafic HTTPS, terminaison TLS 1.3, compression et redirection vers les conteneurs internes.
- **Monitoring & Alertes** : Collecte de métriques via **Prometheus** (latence, RPS, GPU VRAM, erreurs) et tableaux de bord **Grafana** personnalisés. Système d'alerte en temps réel via Webhook (Slack / WhatsApp Business / Email).
- **Sauvegarde et Restauration (Disaster Recovery)** : Sauvegarde quotidienne automatisée des adaptateurs LoRA, configurations, registres et bases de données sur stockage chiffré.
- **Infrastructure as Code (IaC)** :
  - **Helm Chart** : Helm chart pour déploiement Kubernetes à grande échelle.
  - **Module Terraform** : Provisionnement en une commande sur AWS, GCP ou VPS OVH/Hetzner GPU.

---

## 8. NORMES, CONFORMITÉ ET SÉCURITÉ DE L'INFORMATION

### 8.1 Gouvernance et Conformité
- **PRIVACY.md** : Politique de confidentialité stipulant l'anonymisation stricte des données de code traitées.
- **TERMS.md** : Conditions d'utilisation de l'API, garanties SLA et responsabilités d'usage.
- **COMPLIANCE.md** : Conformité aux normes RGPD (anonymisation, droit à l'oubli), ISO 27001 et SOC 2.
- **SBOM (Software Bill of Materials)** : Fichier `SBOM.json` détaillant la liste complète des composants spectraux et dépendances logicielles.
- **Programme Bug Bounty** : Canal informel récompensant le signalement responsable des failles de sécurité.
- **Audit de sécurité externe** : Mandat d'expertise tiers indépendant pour la validation de l'infrastructure API.

---

## 9. DOCUMENTATION COMMUNITY & GOUVERNANCE PROJET

### 9.1 Fichiers de Gouvernance GitHub
- **`CONTRIBUTING.md`** : Directives de contribution, critères d'acceptation du code, gestion des issues et branches.
- **`CODE_OF_CONDUCT.md`** : Code de conduite des contributeurs basé sur le standard Contributor Covenant.
- **`SECURITY.md`** : Protocole de divulgation responsable des vulnérabilités (Email direct sécurisé, clé PGP).
- **Templates Issue & PR** : Modèles structurés `.github/ISSUE_TEMPLATE/` (bug_report.md, feature_request.md) et `.github/PULL_REQUEST_TEMPLATE.md`.
- **`CHANGELOG.md`** : Suivi rigoureux des versions selon le format *Keep a Changelog*.
- **`ROADMAP.md`** : Feuille de route stratégique à 3, 6 et 12 mois pour CyberCode Studio.
- **Badges README** : Badges dynamiques (Statut Build CI, Licence MIT/Model, Python 3.11, Code Size, Docker Downloads).
- **Site MkDocs** : Documentation hébergée sur GitHub Pages via MkDocs Material pour une lecture fluide des guides d'intégration.

### 9.2 Fichiers de Référence Opérationnels
- **`ACKNOWLEDGMENTS.md`** : Remerciements explicites aux projets open source fondateurs (DeepSeek-AI, Hugging Face, PyTorch, vLLM, FastAPI).
- **`FAQ.md` & `TROUBLESHOOTING.md`** : Réponses aux questions fréquentes et guides de résolution des pannes courantes.
- **`PERFORMANCE.md`** : Benchmarks détaillés, temps de réponse TTFT/TPOT, consommations VRAM et techniques d'optimisation.
- **`SECURITY_AUDIT_REPORT.md`** : Synthèse d'audit de sécurité anonymisée.
- **`INCIDENT_RESPONSE.md` & `DISASTER_RECOVERY.md`** : Directives d'intervention d'urgence et plan de reprise d'activité.
- **`SLA.md` & `SUPPORT.md`** : Engagements de disponibilité (99.9%) et modalités du support client.

---

## 10. ÉTHIQUE IA, MODEL CARD ET DATASHEET

### 10.1 Gouvernance des Modèles d'IA
- **Model Card (Fiche Modèle)** : Description détaillée des capacités du modèle DeepSeek-Coder V1 personnalisée par CyberCode Studio, limites d'usage et contextes d'application.
- **Datasheet (Fiche de Données)** : Provenance des données de fine-tuning internes, étapes de nettoyage et procédures d'anonymisation.
- **Déclaration d'Éthique IA** : Engagement pour le développement d'une IA responsable, transparente et respectueuse de la confidentialité des données.
- **Évaluation des Biais & Red Teaming** : Résultats des tests de résistance contre l'injection d'instructions malveillantes (*jailbreaks*) et évaluation des biais du code généré.

---

## 11. ESTIMATION DES COÛTS EN FCFA (XAF)

Estimation budgétaire mensuelle pour l'infrastructure et l'exploitation pour le public local et régional (Taux de conversion fixe : 1 EUR = 655.957 FCFA) :

| Postes de Dépenses | Estimation en Euros (€) | Estimation en FCFA (XAF) |
| :--- | :--- | :--- |
| **VPS GPU Cloud Prod (NVIDIA A10G / RTX 4090)** | 150 € - 300 € / mois | ~100 000 FCFA - 200 000 FCFA / mois |
| **Stockage NVMe Sécurisé (500 Go Chiffré)** | ~30 € / mois | ~20 000 FCFA / mois |
| **Bande passante, Trafic API & Domaines** | ~20 € / mois | ~13 000 FCFA / mois |
| **Total Mensuel Estimé** | **200 € - 350 € / mois** | **~133 000 FCFA - 233 000 FCFA / mois** |

---

## 12. STRATÉGIE COMMERCIALES ET GO-TO-MARKET LOCAL

### 12.1 Visibilité & Interfaces Utilisateur
- **Interface Web Démos** : IHM conviviale permettant aux prospects de tester l'audit de sécurité sans écriture de code.
- **Extension VS Code & Plugin Navigateur** : Intégration de l'audit de sécurité directement dans l'environnement de développement du client.
- **Chatbot Web** : Agent virtuel d'assistance technique et commerciale sur le site CyberCode Studio.

### 12.2 Stratégie Marketing & Écosystème Local
- **Présence Réseaux & Médias** : Page officielle LinkedIn CyberCode Studio, chaîne YouTube de démonstration, articles de blog techniques (Medium, Dev.to).
- **Newsletter & Offres de Lancement** : Offre exclusive de lancement : *5 audits de sécurité gratuits pour les 5 premières entreprises partenaires*.
- **Écosystème & Communauté** : Organisation d'ateliers et webinaires sur la cybersécurité et le devsecops à Pointe-Noire, Brazzaville et en ligne.
- **Tarification Transparente** : Formules sur mesure (Audit à l'acte, Abonnement API, Intégration Entreprise) adaptées au marché local.

---

## 13. PLAN D'EXÉCUTION TECHNIQUE

1. **Étape 1** : Modernisation des dépendances dans `requirements.txt` et élimination d'`attrdict`.
2. **Étape 2** : Extension de `finetune/finetune_deepseekcoder.py` avec le support LoRA/QLoRA (PEFT) et création du script de fusion `merge_peft_adapters.py`.
3. **Étape 3** : Rendre `demo/app.py` 100% autonome sans dépendance obligatoire à HF ZeroGPU spaces.
4. **Étape 4** : Développement de l'API OpenAI-compatible (`serve/api_server.py`) et de l'engine d'audit (`serve/security_audit.py`).
5. **Étape 5** : Rédaction des Dockerfiles, docker-compose, scripts de tests unitaires et workflows CI/CD GitHub Actions.
6. **Étape 6** : Rédaction des documents de gouvernance, de sécurité et d'éthique (`CONTRIBUTING.md`, `SECURITY.md`, `PRIVACY.md`, `TERMS.md`, `COMPLIANCE.md`, `SBOM.json`).
7. **Étape 7** : Validation complète de la suite de tests et vérification formelle de la non-régression V1.

---

*Document de spécification technique officiel CyberCode Studio - Tous droits réservés.*
