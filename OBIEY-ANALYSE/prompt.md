# CAHIER DES CHARGES COMPLET ET STRUCTURÉ – VERSION PERSONNALISÉE DEEPSEEK-CODER POUR CYBERCODE STUDIO

> **Directive principale** : Ce document guide une IA ou une équipe de développement dans la modernisation, la sécurisation et l’extension du projet DeepSeek-Coder V1, afin d’en faire une **solution personnalisée pour CyberCode Studio**. Toutes les fonctionnalités existantes (scripts d’évaluation, fine-tuning DeepSpeed Zero-3, démo Gradio) doivent être **rigoureusement préservées et rester rétrocompatibles**. **Aucune migration vers DeepSeek-Coder-V2, V3 ou R1 n’est autorisée.**

---

## 1. CONTEXTE ET OBJECTIF

Le dépôt actuel fournit la baseline officielle de **DeepSeek-Coder V1**. Bien que fonctionnel pour la recherche et la démonstration, il souffre d’obsolescences :
- Dépendances Python de fin 2023 (`transformers==4.35.0`, `attrdict`).
- Pas de support LoRA / QLoRA.
- Pas d’API OpenAI-compatible.
- Pas de conteneurisation Docker.
- Pas de tests unitaires ni de CI/CD.

**Objectif** : Élever ce projet aux standards logiciels industriels modernes (2024-2025) et le transformer en une **version personnalisée sur mesure pour CyberCode Studio**, une startup spécialisée dans le développement logiciel, web, mobile et la cybersécurité sur mesure.

La version personnalisée doit intégrer :
- Le **fine-tuning LoRA/QLoRA** sur données internes anonymisées.
- Des **modules de cybersécurité** (audit, génération de code sécurisé, revue de code).
- Une **API interne sécurisée** compatible OpenAI.
- Une **intégration CI/CD** avec revue de sécurité automatisée.
- Une **conteneurisation Docker** complète et un déploiement VPS.

**Contrainte absolue** : Utiliser **exclusivement les poids V1** (`deepseek-ai/deepseek-coder-1.3b-instruct`, `deepseek-ai/deepseek-coder-6.7b-instruct`, `deepseek-ai/deepseek-coder-33b-instruct`). **Interdiction de télécharger, charger ou référencer les poids V2, V3, R1 ou tout autre modèle dérivé.**

---

## 2. RÈGLES ET CONTRAINTES STRICTES

1. **Conservation du code existant** : Ne supprime aucun fichier ni aucun comportement existant. Toutes les améliorations doivent être apportées par refactorisation non-cassante ou par ajout de nouvelles options/modules.
2. **Compatibilité descendante** : Les commandes et scripts du `README.md` original doivent continuer de fonctionner à 100 %.
3. **Verrouillage absolu sur la V1** : Ajouter des constantes explicites (`MODEL_NAME = "deepseek-ai/deepseek-coder-6.7b-instruct"`) et interdire tout téléchargement de poids V2+.
4. **Non-régression** : Toute mise à jour de dépendance doit être validée par des tests sur les poids V1.
5. **Modularité et réutilisabilité** : Le code doit être découpé en briques modulaires (fonctions autonomes, classes isolées, modules spécialisés, blocs de code réutilisables). Code typé (type hints), docstrings, gestion d’exceptions explicite.
6. **Pratique de test** : Tout nouveau composant doit être accompagné de ses tests unitaires.
7. **Personnalisation métier** : Le code doit refléter l’expertise de CyberCode Studio (cybersécurité, développement, conformité).
8. **Sécurité by design** : Authentification, rate limiting, logs, monitoring, anonymisation des données clients.

---

## 3. CAHIER DES CHARGES DES AMÉLIORATIONS

### 3.1. Modernisation des dépendances, versions testées et matrice de compatibilité

**Versions exactes testées et validées avec DeepSeek-Coder V1** :
- `transformers` >= 4.40.0 (version recommandée : 4.41.2)
- `torch` >= 2.2.0 (version recommandée : 2.3.0+cu121)
- `vllm` >= 0.4.0 (version recommandée : 0.4.2)
- `cuda` >= 12.1 (versions supportées : CUDA 12.1 / 12.2)
- `peft` >= 0.10.0
- `bitsandbytes` >= 0.43.0
- `fastapi` >= 0.110.0
- `pydantic` >= 2.7.0

**Matrice de compatibilité** :

| Composant | Version minimale | Version recommandée | Environnement cible |
| :--- | :--- | :--- | :--- |
| **Python** | 3.10 | 3.11 | Linux Ubuntu 22.04 LTS |
| **PyTorch** | 2.2.0 | 2.3.0 | CUDA 12.1 / 12.2 |
| **Transformers** | 4.40.0 | 4.41.2 | Hugging Face Hub V1 |
| **vLLM** | 0.4.0 | 0.4.2 | Inférence haute performance |
| **PEFT / LoRA** | 0.10.0 | 0.11.1 | QLoRA 4-bit / 8-bit |
| **CUDA Driver** | 535.x | 550.x | NVIDIA A10G / A100 / RTX 4090 |

**Nettoyage et modularité des dépendances** :
- Supprimer `attrdict` et le remplacer par des `dataclasses` Python natives ou `Pydantic`.
- Créer des fichiers de dépendances modulaires :
  - `requirements.txt` (base)
  - `requirements-finetune.txt` (PEFT, DeepSpeed, BitsAndBytes)
  - `requirements-serve.txt` (FastAPI, vLLM)
  - `requirements-dev.txt` (pytest, ruff, black)

### 3.2. Extension du module de fine-tuning (`finetune/finetune_deepseekcoder.py`)

**Support LoRA / QLoRA (PEFT)** :
- Ajouter les arguments CLI : `--use_peft` (bool), `--lora_r` (int, default=16), `--lora_alpha` (int, default=32), `--lora_dropout` (float, default=0.05), `--lora_target_modules` (list).
- Permettre le chargement en quantification 4-bit / 8-bit (`bitsandbytes`) pour QLoRA.
- Conserver le mode Full Fine-Tuning DeepSpeed ZeRO-3 par défaut si `--use_peft` n’est pas activé.

**Sécurisation multi-core CPU** :
- Remplacer `num_proc=32` codé en dur par `min(32, os.cpu_count() or 1)`.

**Script de fusion** :
- Ajouter `finetune/merge_peft_adapters.py` pour fusionner les poids LoRA avec le modèle de base.

### 3.3. Robustesse et autonomie du module démo (`demo/app.py`)

- Rendre l’import de `spaces` (Hugging Face ZeroGPU) optionnel via `try...except ImportError`.
- Détecter automatiquement le device (`cuda`, `mps`, `cpu`).
- Ajouter des protections contre les erreurs VRAM / OOM GPU.
- Assurer la compatibilité avec Gradio v4 et v5.

### 3.4. Serveur d’API production-ready (`serve/`)

- Créer `serve/api_server.py` avec `FastAPI` + `uvicorn`.
- Interface compatible OpenAI v1 :
  - `POST /v1/chat/completions`
  - `POST /v1/completions` (avec support FIM / Fill-In-the-Middle)
  - `GET /v1/models`
- Script alternatif haute performance `serve/vllm_server.py` intégrant `vLLM`.

### 3.5. Conteneurisation et déploiement Docker

- `Dockerfile` basé sur `nvidia/cuda:12.1.1-devel-ubuntu22.04`, préconfiguré pour PyTorch, Transformers et CUDA.
- `docker-compose.yml` avec services :
  - `demo` (Gradio)
  - `api` (FastAPI OpenAI-compatible)
  - `finetune` (entraînement)
  - `security-audit` (module cybersécurité)

### 3.6. Assurance qualité, tests unitaires et CI/CD

- Créer `tests/` :
  - `test_tokenizer.py` : tokens FIM (`<｜fim begin｜>`, `<｜fim hole｜>`, `<｜fim end｜>`) et EOT.
  - `test_templates.py` : templates d’instructions et de chat.
  - `test_security_audit.py` : détection de vulnérabilités connues.
  - `test_api_security.py` : authentification, rate limiting, logs.
  - `test_finetune_cybercode.py` : fine-tuning LoRA sur petit jeu de données.
- Workflow GitHub Actions `.github/workflows/ci.yml` : linting (`ruff`) + tests (`pytest`).

### 3.7. Renforcement de la sécurité et conformité RGPD

**Gestion centralisée des secrets** :
- Intégration avec **HashiCorp Vault** ou **AWS Secrets Manager** pour l'injection sécurisée des clés API, jetons JWT et certificats TLS. Aucune clé ne doit figurer dans les fichiers de configuration ou le code.

**Chiffrement des données** :
- **Au repos** : Chiffrement AES-256 (LUKS / AWS KMS) pour les jeux de données, adaptateurs LoRA et fichiers de logs.
- **En transit** : TLS 1.3 obligatoire sur toutes les communications API et inter-services Docker.

**Conformité RGPD & Confidentialité** :
- **Consentement & Anonymisation** : Pipeline automatique de nettoyage des données d'entraînement (suppression des noms, adresses IP, identifiants, clés d'API).
- **Droit à l’oubli** : Mécanisme de retrait des extraits de code clients sur demande du jeu de données de fine-tuning.
- **Journalisation d'accès sécurisée** : Traçabilité des requêtes d'API (horodatage, ID utilisateur, hash de requête) sans stockage du code source client en clair.

### 3.8. Tests de non-régression automatisés

- Comparaison des sorties du modèle V1 avant/après chaque modification sur un jeu d'instructions de référence (*benchmark set*).
- Validation de la fidélité des complétions de code, du respect des tokens FIM et du format JSON de sortie.
- Intégration automatique de cette comparaison dans le pipeline CI (`.github/workflows/ci.yml`).

### 3.9. Tests de charge, performance et seuils d'acceptation

**Mesures exigées** :
- Temps de réponse (Latence TTFT - *Time To First Token* et TPOT - *Time Per Output Token*).
- Consommation VRAM et RAM sous charge.
- Débit global de l'API (RPS / tokens par seconde).

**Seuils d'acceptation (SLA)** :
- Latence au premier token : < 300 ms (modèle 6.7B sur RTX 4090 / A10G).
- Consommation VRAM maximale : < 14 Go (modèle 6.7B en FP16) / < 8 Go (en QLoRA 4-bit).
- Taux d'erreur API : < 0.1 % sous charge de 100 requêtes simultanées.

### 3.10. Plan de rollback et stratégie de repli

- Stratégie de déploiement *Blue-Green* ou *Canary* lors de la mise à jour des conteneurs ou des poids LoRA.
- Sauvegarde systématique de la version précédente de l'API et des adaptateurs PEFT.
- Procédure de retour arrière automatique en cas d'échec du healthcheck (`/healthz`) de la nouvelle version dans un délai de 60 secondes.

### 3.11. Estimation des coûts et analyse comparative (vLLM vs Ollama)

**Estimation des coûts d'infrastructure** :
- VPS / Cloud GPU (ex. NVIDIA A10G / RTX 4090) : ~150 € à 300 € / mois.
- Stockage sécurisé (SSD NVMe 500 Go chiffrement repos) : ~30 € / mois.
- Bande passante & trafic API : ~20 € / mois.

**Comparatif vLLM vs Ollama pour l'API CyberCode Studio** :

| Critère | vLLM | Ollama | Choix retenu |
| :--- | :--- | :--- | :--- |
| **Débit (Tokens/s)** | Très élevé (PagedAttention) | Moyen | **vLLM** (Production) |
| **Contrôle API / FIM** | Total (FastAPI natif) | Simplifié | **vLLM** / **FastAPI** |
| **Support LoRA dynamique** | Oui | Limité | **vLLM** |
| **Usage recommandé** | Serveur de production VPS | Test local développeur | Dual (vLLM prod / Ollama dev) |

### 3.12. Documentation des procédures d'urgence (*Incident Response*)

Procédures documentées pour l'équipe technique :
1. **Fuite de données ou secrets exposés** : Révocation immédiate des clés API via Vault/AWS KMS, rotation des jetons, purge des caches et notification des équipes conformité.
2. **Attaque ou surcharge DoS/DDoS** : Activation du rate-limiting strict à la passerelle reverse-proxy (Nginx / Traefik), blocage IP et bascule en mode dégradé.
3. **Modèle ou adaptateur compromis** : Isolation immédiate du conteneur, rollback vers la version antérieure validée et déclenchement d'un audit de sécurité des poids.

### 3.13. Conception briques modulaires et réutilisables

Chaque composant du système doit être structuré sous forme de briques autonomes :
- **Classes réutilisables** : Encapsulation des requêtes d'audit, de la gestion des tokenizers, des validateurs Pydantic.
- **Fonctions pures et autonomes** : Modules de nettoyage de code, de calcul dynamique de cœurs CPU, de formatage d'instructions.
- **Modules isolés** : Séparation stricte entre les couches Inférence (`serve/`), Fine-tuning (`finetune/`), Audit (`serve/security_audit.py`) et Interfaces (`demo/`).

### 3.14. Module d’audit de sécurité (`serve/security_audit.py`)

- **Fonction** : Analyser du code (Python, Java, C++, JS, PHP, etc.) et détecter les vulnérabilités : injections SQL, XSS, CSRF, mauvaise gestion des sessions, secrets exposés, etc.
- **Entrée** : Code source + langage.
- **Sortie** : Rapport JSON structuré :
  - Liste des vulnérabilités (type, ligne, gravité faible/moyenne/élevée/critique).
  - Recommandations de correctifs.
  - Score de sécurité.
- **Consigne système intégrée** :
  ```text
  Tu es un expert en cybersécurité chez CyberCode Studio. Analyse le code suivant et identifie les vulnérabilités potentielles. Pour chaque faille, indique la ligne, le type, la gravité (faible/moyenne/élevée/critique) et propose un correctif précis.
  Code : {code}
  Langage : {langage}
  ```

### 3.15. Génération de code sécurisé

- Modèles de consignes pour générer du code respectant OWASP Top 10.
- Exemple :
  ```text
  Génère une fonction {langage} pour {tâche} en appliquant les règles de sécurité suivantes : validation des entrées, échappement des sorties, requêtes paramétrées, gestion sécurisée des erreurs.
  ```

### 3.16. Revue de code automatisée (CI/CD)

- Intégration dans GitHub Actions / GitLab CI.
- À chaque Pull Request, le modèle analyse le diff et poste un commentaire :
  - Problèmes de sécurité détectés.
  - Suggestions d’amélioration.
  - Résumé exécutif.
- Exemple de workflow :
  ```yaml
  - name: Security Review
    run: |
      curl -X POST http://vps-ip:8000/v1/security/audit \
        -H "Authorization: Bearer ${{ secrets.API_KEY }}" \
        -d '{"code": "${{ github.event.pull_request.diff }}", "langage": "auto"}'
  ```

### 3.17. API interne sécurisée (`serve/api_server.py`)

**Endpoints supplémentaires** :
- `POST /v1/security/audit` : audit de sécurité.
- `POST /v1/code/review` : revue de code.
- `POST /v1/code/generate` : génération de code sécurisé.

**Sécurité** :
- Authentification par clé API (`Authorization: Bearer <token>`).
- Rate limiting (ex. 100 req/min).
- Logs des requêtes (sans stocker le code client en clair).
- Monitoring via Prometheus / Grafana.

**Exemple FastAPI** :
```python
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="Authorization")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != f"Bearer {settings.API_KEY}":
        raise HTTPException(status_code=403, detail="Accès refusé")
```

### 3.18. Fine-tuning sur données internes (`finetune/finetune_cybercode.py`)

**Collecte et anonymisation** :
- Extraits de code clients (avec accord), rapports d’audit, bonnes pratiques internes.
- Script d’anonymisation : suppression des noms de projets, IP, identifiants.

**Entraînement LoRA / QLoRA** :
- Utiliser les arguments PEFT déjà ajoutés (`--use_peft`, `--lora_r`, etc.).
- Exemple :
  ```bash
  python finetune/finetune_cybercode.py \
    --model_name_or_path deepseek-ai/deepseek-coder-6.7b-instruct \
    --data_path ./data/cybercode_dataset.json \
    --use_peft --lora_r 16 --lora_alpha 32 \
    --output_dir ./models/cybercode-lora
  ```

**Pipeline de fine-tuning continu** :
- Collecte mensuelle des retours utilisateurs (via API).
- Ré-entraînement automatique sur les nouvelles données.
- Évaluation sur benchmarks internes (sécurité, qualité de code).
- Déploiement automatique de la nouvelle version LoRA.

### 3.19. Intégration IDE (VS Code)

- Extension VS Code légère appelant l’API interne pour :
  - Audit de sécurité en temps réel.
  - Suggestions de correctifs.
  - Génération de tests unitaires sécurisés.
- Utilise les endpoints `/v1/security/audit` et `/v1/code/generate`.

### 3.20. Documentation et formation

- Guide d’utilisation pour les équipes internes (développeurs, auditeurs).
- Procédures de fine-tuning continu et de mise à jour du modèle.
- Section « Migration depuis V1 » dans le README.

---

## 4. PLAN D’EXÉCUTION

1. **Étape 1** : Moderniser `requirements.txt`, fixer les versions exactes et nettoyer les dépendances obsolètes.
2. **Étape 2** : Étendre `finetune/finetune_deepseekcoder.py` avec PEFT / LoRA / QLoRA.
3. **Étape 3** : Rendre `demo/app.py` 100 % autonome et compatible local / HF Spaces.
4. **Étape 4** : Implémenter le serveur FastAPI / vLLM dans `serve/` sous forme de briques modulaires.
5. **Étape 5** : Écrire les Dockerfiles, tests unitaires et workflow GitHub Actions (avec tests de non-régression).
6. **Étape 6** : Exécuter la suite de tests et vérifier la non-régression sur V1.
7. **Étape 7** : Verrouiller l’usage des poids V1 dans tous les scripts (constantes `MODEL_NAME`).
8. **Étape 8** : Implémenter `serve/security_audit.py` et les endpoints associés.
9. **Étape 9** : Sécuriser l’API (Vault/AWS KMS, chiffrement, RGPD, clé API, rate limiting, logs, monitoring).
10. **Étape 10** : Créer `finetune/finetune_cybercode.py` et le pipeline de fine-tuning continu.
11. **Étape 11** : Intégrer la revue de code dans GitHub Actions / GitLab CI.
12. **Étape 12** : Développer l’extension VS Code (ou un script CLI).
13. **Étape 13** : Rédiger la documentation interne, les procédures de sécurité et le plan d'urgence.
14. **Étape 14** : Exécuter tous les tests (unitaires, intégration, charge, non-régression) et valider le déploiement VPS / rollback.

---

## 5. LIVRABLES ATTENDUS

- Code source modifié + nouveaux modules briques réutilisables :
  - `serve/api_server.py`, `serve/vllm_server.py`, `serve/security_audit.py`
  - `finetune/finetune_cybercode.py`, `finetune/merge_peft_adapters.py`
- `Dockerfile` et `docker-compose.yml` mis à jour (services `demo`, `api`, `finetune`, `security-audit`).
- Fichiers de requirements modulaires (`requirements-serve.txt`, `requirements-finetune.txt`, etc.).
- Tests unitaires, d'intégration, de non-régression et de charge (`tests/`).
- Workflow CI/CD GitHub Actions avec étape de revue de sécurité et tests automatisés.
- Documentation : README mis à jour, guide d’utilisation CyberCode Studio, procédures d'urgence, plan de rollback, comparatif de coûts.
- Rapport de non-régression sur le modèle V1.

---

## 6. FORMAT DE RÉPONSE ATTENDU

- Explications étape par étape.
- Blocs de code complets et modulaires pour chaque fichier (chemin indiqué).
- Commandes shell prêtes à l’emploi.
- Avertissements sur les incompatibilités et les ressources nécessaires (VRAM, RAM).
- Si une étape est impossible sans le dépôt V2, proposer une alternative basée sur les poids V1 et des bibliothèques tierces (vLLM, TGI, PEFT).

---

*En appliquant ce cahier des charges, le projet DeepSeek-Coder passera d’un dépôt de recherche statique à une **solution personnalisée, moderne, sécurisée, conteneurisée, modulaire et prête pour la production**, taillée sur mesure pour CyberCode Studio, sans jamais migrer vers V2.*
