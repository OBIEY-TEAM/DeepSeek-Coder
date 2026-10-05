# PROMPT COMPLET ET STRUCTURÉ POUR L'AMÉLIORATION DU PROJET DEEPSEEK-CODER

> **Directive principale** : Ce prompt est conçu pour guider une IA ou une équipe de développement dans la modernisation, la sécurisation et l'extension du projet DeepSeek-Coder. **Toutes les fonctionnalités existantes (scripts d'évaluation, fine-tuning DeepSpeed Zero-3, démo Gradio) doivent être rigoureusement préservées et rester rétrocompatibles.**

---

## CONTEXTE ET OBJECTIF

Le dépôt actuel fournit la baseline officielle de DeepSeek-Coder (v1). Bien que fonctionnel pour la recherche et la démonstration, il souffre d'obsolescences (dépendances Python 2023, pas de support LoRA/QLoRA, pas d'API OpenAI-compatible, pas de conteneurisation Docker, pas de tests unitaires).

L'objectif est d'élever ce projet aux standards logiciels industriels modernes (2024-2025) en intégrant les recommandations synthétisées dans `OBIEY-ANALYSE/analyse.md` et `OBIEY-ANALYSE/prompt-amelioration.md`.

---

## RÈGLES ET CONTRAINTES STRICTES

1. **Conservation du Code Existant** : Ne supprime aucun fichier ni aucun comportement existant. Toutes les améliorations doivent être apportées par refactorisation non-cassante ou par ajout de nouvelles options/modules.
2. **Compatibilité Descendante** : Les commandes et scripts présentés dans le `README.md` original doivent continuer de fonctionner à 100%.
3. **Modularité** : Le nouveau code doit être proprement découpé (typage Python, docstrings, gestion d'exceptions explicite).
4. **Pratique de Test** : Tout nouveau composant doit être accompagné de ses tests unitaires.

---

## CAHIER DES CHARGES DES AMÉLIORATIONS À EFFECTUER

### 1. Modernisation des Dépendances et de la Configuration (`requirements.txt`)
* Mettre à jour `requirements.txt` pour lever la restriction stricte `transformers==4.35.0` et supporter `transformers>=4.40.0`.
* Supprimer la dépendance obsolète `attrdict` et remplacer son usage par des `dataclasses` native Python ou `Pydantic`.
* Ajouter les dépendances optionnelles pour le fine-tuning léger et l'inférence optimisée : `peft`, `bitsandbytes`, `vllm`, `fastapi`, `uvicorn`, `pydantic`.
* Créer des fichiers de dépendances modulaires :
  - `requirements.txt` (base)
  - `requirements-finetune.txt` (PEFT, DeepSpeed, BitsAndBytes)
  - `requirements-serve.txt` (FastAPI, vLLM)
  - `requirements-dev.txt` (pytest, ruff, black)

### 2. Extension du Module de Fine-Tuning (`finetune/finetune_deepseekcoder.py`)
* **Support LoRA / QLoRA (PEFT)** :
  - Ajouter les arguments CLI `--use_peft` (bool), `--lora_r` (int, default=16), `--lora_alpha` (int, default=32), `--lora_dropout` (float, default=0.05), `--lora_target_modules` (list).
  - Permettre le chargement du modèle en quantification 4-bit / 8-bit (`bitsandbytes`) pour le QLoRA.
  - Conserver le mode Full Fine-Tuning DeepSpeed ZeRO-3 par défaut si `--use_peft` n'est pas activé.
* **Sécurisation Multi-Core CPU** :
  - Remplacer le `num_proc=32` codé en dur dans `train_dataset.map(...)` par une valeur calculée dynamiquement (`min(32, os.cpu_count() or 1)`).
* **Script de Fusion (Merge)** :
  - Ajouter un script `finetune/merge_peft_adapters.py` pour fusionner les poids LoRA sauvegardés avec le modèle de base.

### 3. Robustesse et Autonomie du Module Démo (`demo/app.py`)
* Rendre l'import de `spaces` (Hugging Face ZeroGPU) optionnel via un bloc `try...except ImportError`.
* Détecter automatiquement le device d'exécution (`cuda`, `mps`, ou `cpu`).
* Ajouter des mécanismes de protection contre les erreurs d'incompatibilité de VRAM / OOM GPU.
* Mettre à jour la gestion de l'interface Gradio pour assurer la compatibilité avec Gradio v4 et v5.

### 4. Création d'un Serveur d'API Production-Ready (`serve/`)
* Créer un module `serve/api_server.py` utilisant `FastAPI` et `uvicorn`.
* Proposer une interface API compatible OpenAI v1 :
  - `POST /v1/chat/completions`
  - `POST /v1/completions` (supportant la complétion FIM / Fill-In-the-Middle)
  - `GET /v1/models`
* Proposer un script alternatif d'inférence haute performance `serve/vllm_server.py` intégrant `vLLM`.

### 5. Conteneurisation et Déploiement Docker
* Créer un `Dockerfile` basé sur `nvidia/cuda:12.1.1-devel-ubuntu22.04` préconfiguré pour PyTorch, Transformers et CUDA.
* Créer un `docker-compose.yml` avec plusieurs services :
  - `demo` (Interface Gradio)
  - `api` (Serveur FastAPI OpenAI-compatible)
  - `finetune` (Environnement d'entraînement)

### 6. Assurance Qualité, Tests et CI/CD
* Créer un dossier `tests/` contenant :
  - `test_tokenizer.py` : Vérification du bon traitement des tokens spéciaux FIM (`<｜fim begin｜>`, `<｜fim hole｜>`, `<｜fim end｜>`) et EOT (`<|EOT|>`).
  - `test_prompts.py` : Validation du format des templates d'instructions et de chat.
  - `test_api.py` : Tests d'intégration de l'API FastAPI.
* Ajouter un workflow GitHub Actions `.github/workflows/ci.yml` exécutant le linting (`ruff`) et la suite de tests `pytest`.

---

## PLAN D'EXÉCUTION SUGGÉRÉ

1. **Étape 1** : Moderniser `requirements.txt` et nettoyer les dépendances obsolètes.
2. **Étape 2** : Étendre `finetune/finetune_deepseekcoder.py` avec le support PEFT / LoRA / QLoRA.
3. **Étape 3** : Rendre `demo/app.py` 100% autonome et compatible local/HF Spaces.
4. **Étape 4** : Implémenter le serveur FastAPI / vLLM dans `serve/`.
5. **Étape 5** : Écrire les Dockerfiles, les tests unitaires et le workflow GitHub Actions.
6. **Étape 6** : Exécuter la suite de tests et vérifier la non-régression de l'existant.

---

*En appliquant ce prompt, le projet DeepSeek-Coder passera d'un dépôt de recherche statique à une solution logicielle complète, moderne, conteneurisée et prête pour la production.*
