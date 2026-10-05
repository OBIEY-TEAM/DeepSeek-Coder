# Propositions d'Améliorations et de Corrections du Projet DeepSeek-Coder

Ce document détaille l'ensemble des axes d'amélioration, des corrections de bugs et des modernisations architecturales à apporter au projet sans altérer l'existant.

---

## 1. Modernisation des Dépendances & Compatibilité Système

### 1.1. Dépendances Racine (`requirements.txt`)
* **Problème** : `transformers==4.35.0` et `attrdict` sont obsolètes et bloquent l'utilisation de PyTorch 2.2+, CUDA 12.x ou Python 3.10+.
* **Propositions** :
  - Mettre à jour `transformers` vers une version récente (ex: `>=4.40.0`).
  - Supprimer `attrdict` ou le remplacer par `pydantic` ou des `dataclasses` native Python.
  - Ajouter `peft` pour le support du fine-tuning léger (LoRA/QLoRA).
  - Ajouter `bitsandbytes` et `triton` pour la quantification et l'optimisation mémoire.
  - Structurer les dépendances par profils (ex. `requirements.txt`, `requirements-dev.txt`, `requirements-eval.txt`).

---

## 2. Optimisation du Module de Fine-Tuning (`finetune/`)

### 2.1. Support de LoRA, QLoRA et PEFT
* **Problème** : `finetune_deepseekcoder.py` ne permet actuellement que le Full Fine-Tuning via DeepSpeed ZeRO-3, ce qui nécessite plusieurs GPU de 80 Go VRAM.
* **Propositions** :
  - Intégrer la bibliothèque `peft` de Hugging Face dans `finetune_deepseekcoder.py`.
  - Ajouter des arguments CLI pour activer LoRA/QLoRA (`--use_peft`, `--lora_r`, `--lora_alpha`, `--lora_dropout`, `--quantization 4bit|8bit`).
  - Permettre l'enregistrement séparé des adaptateurs LoRA et la fusion (*merge*) des poids avec le modèle de base.

### 2.2. Robustesse et Gestion Multi-GPU / Multi-CPU
* **Problème** : Le paramètre `num_proc=32` dans `raw_train_datasets.map(...)` est codé en dur, risquant de faire planter l'exécution sur des machines possédant moins de cœurs CPU.
* **Propositions** :
  - Calculer dynamiquement le nombre de processus de prétraitement : `min(32, os.cpu_count() or 1)`.
  - Prendre en charge le streaming des datasets (`streaming=True`) pour traiter de très grands jeux de données sans surcharge RAM CPU.

---

## 3. Amélioration du Module de Démonstration (`demo/`)

### 3.1. Abstraction pour l'Exécution Locale et Multi-Plateforme
* **Problème** : `demo/app.py` utilise l'importation `@spaces.GPU` spécifique à la plateforme Hugging Face Spaces. En exécution locale, ce décorateur peut échouer ou provoquer des avertissements.
* **Propositions** :
  - Rendre l'import de `spaces` optionnel avec un bloc `try...except ImportError`.
  - Ajouter la détection automatique des cartes GPU et un fallback propre sur CPU ou Apple Silicon (MPS).
  - Mettre à jour Gradio vers v4/v5 avec la gestion moderne des états de conversation (`gr.Chatbot(type="messages")`).
  - Ajouter le contrôle du paramètre `Temperature` et `Max Tokens` en direct sur l'IHM.

---

## 4. Normalisation et Modernisation de l'Inférence & API

### 4.1. Création d'un Serveur d'API Production Ready (FastAPI + vLLM)
* **Problème** : Le projet ne contient aucun serveur d'API standard (ex. OpenAI-compatible API) pour intégrer le modèle à des extensions IDE (VSCode, JetBrains, Continue.dev, Cursor).
* **Propositions** :
  - Ajouter un module `serve/` ou `api/` contenant un serveur FastAPI léger exposant les points de terminaison `/v1/chat/completions` et `/v1/completions`.
  - Proposer un script de lancement basé sur `vLLM` pour l'inférence à haut débit avec du Tensor Parallelism.

---

## 5. Industrialisation, Conteneurisation & CI/CD

### 5.1. Dockerisation
* **Propositions** :
  - Créer un `Dockerfile` optimisé pour NVIDIA CUDA 12.x avec PyTorch préinstallé.
  - Créer un `docker-compose.yml` permettant de lancer facilement la démo Gradio, l'API FastAPI et vLLM.

### 5.2. Qualité de Code, Tests et CI/CD
* **Propositions** :
  - Ajouter des tests unitaires (`tests/`) vérifiant :
    * La tokenisation et la gestion des tokens FIM (`<｜fim begin｜>`, `<｜fim hole｜>`, `<｜fim end｜>`).
    * Le formatage des templates de chat.
    * Le chargement des configurations et des données de fine-tuning.
  - Mettre en place un workflow GitHub Actions (`.github/workflows/ci.yml`) pour vérifier le linting (`ruff`/`black`) et exécuter les tests unitaires à chaque commit.

---

## 6. Prise en Charge des Nouvelles Générations de Modèles (DeepSeek-Coder-V2 / V3)

* **Propositions** :
  - Étendre la compatibilité du tokenizer et du modèle pour prendre en charge les modèles d'architecture Mixture of Experts (MoE) comme DeepSeek-Coder-V2 et V3.
  - Mettre à jour les scripts d'évaluation pour supporter l'inférence distribuée multi-nodes pour les modèles de grande taille.

---

## 7. Synthèse des Actions Prioritaires

1. **Priorité 1 (Critique)** : Mise à jour de `requirements.txt` et élimination des dépendances obsolètes (`attrdict`).
2. **Priorité 2 (Haute)** : Ajout du support LoRA / QLoRA dans `finetune/finetune_deepseekcoder.py`.
3. **Priorité 3 (Moyenne)** : Correction de `demo/app.py` pour un fonctionnement autonome sans dépendance obligatoire à HF Spaces.
4. **Priorité 4 (Avancée)** : Ajout d'une API OpenAI-compatible via FastAPI/vLLM, conteneurisation Docker et mise en place de tests unitaires.
