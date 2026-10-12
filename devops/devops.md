# 🚀 GUIDE DEVOPS, ANÁLYSE DU PROJET & DÉPLOIEMENT CYBERSOCLE

---

## 1. 🔍 ANALYSE APPROFONDIE DU PROJET CYBERSOCLE

**CYBERSOCLE** est une plateforme hybride de cybersécurité industrielle combinant la micro-segmentation réseau eBPF, la conteneurisation immuable durcie, une passerelle SSH de déception (honeypot dynamique), un EDR sidecar, un registre de logs immuable Merkle Ledger, de l'intelligence artificielle locale hors-ligne (LLM offline-first), de l'analyse vectorielle Qdrant, la validation formelle de vaccins de sécurité, et une architecture multi-entreprises à preuves ZKP (Zero-Knowledge Proofs).

### 🏛️ Le Concept Fondateur des 5 Bateaux
Dans CYBERSOCLE, chaque environnement (qu'il s'agisse d'un VPS d'Entreprise Cliente ou du VPS LAB Central géré par **OBIEY Christ Dany**) est découpé en **5 Bateaux principaux** hermétiques :
1. **Bateau OFFICIEL** : Zone de production hébergeant les cellules utilisateur légitimes (`mike-vrai`).
2. **Bateau PRISON** : Zone de quarantaine sandbox / pot de miel (honeypot) pour isoler les attaquants, malwares et sessions suspectes (`mike-faux`).
3. **Bateau MODELE** : Container maître hybride hébergeant le LLM principal en mode 100% hors-ligne (`offline-first`). Accès en **lecture seule strict** (`--read-only`, `tmpfs`) aux volumes de données.
4. **Bateau SCIENCE (Threat-Intel-Lab)** : Container hébergeant la base vectorielle Qdrant et le moteur de synthèse de vaccins. Relié **uniquement** au Bateau MODELE via un réseau privé restreint (`internal: true`).
5. **Bateau TEST** : Zone d'expérimentation isolée permettant de tester la viabilité, la syntaxe AST, la sécurité (Bandit) et l'impact de performance des vaccins de sécurité générés.

---

### 🌐 Réseau Privé, Micro-segmentation eBPF et Isolation
- **Réseau Virtuel Privé** : `reseau-prive` (`driver: bridge`, `internal: true`, `enable_icc: false`).
- **Addressing IP Statique** :
  - Passerelle : `172.28.0.1` | OFFICIEL : `172.28.0.10` | PRISON : `172.28.0.20` | MODELE : `172.28.0.30` | SCIENCE : `172.28.0.40` | TEST : `172.28.0.50`.
- **Règles eBPF Cilium CNI** : Filtrage au niveau du noyau Linux (L3/L4/L7). Le Bateau SCIENCE ne communique qu'avec MODELE.
- **Durcissement des Cellules** : cgroups v2 (RAM max 2 Go par cellule), mode Docker Rootless, profil Seccomp (`SCMP_ACT_ERRNO`), AppArmor (`deny /sys/firmware/**`, `deny /proc/kcore`), système de fichiers racine en lecture seule (`--read-only`), et microVMs Firecracker pour le Bateau PRISON.

---

### 🔑 Authentification Multi-Facteurs & Passerelle SSH de Déception
- **Routage Dynamique** :
  - **`mike-vrai`** (Mot de passe + Clé locale + TPM 2.0 valide + Score d'anomalie IA < 0.60) $\rightarrow$ Accès à sa cellule saine sur le Bateau OFFICIEL + Tunnel VPN Entreprise.
  - **`mike-faux`** (Anomalie détectée, clé/TPM invalide ou score IA $\ge$ 0.60) $\rightarrow$ Redirection transparente vers la cellule leurre du Bateau PRISON (honeypot dynamique alimenté par le LLM et truffé de Canary Tokens). Accès VPN refusé.

---

### 📜 Logging Unidirectionnel Falco & Merkle Ledger
- **Sidecar Espion Falco (eBPF)** : Surveillance temps réel des `syscalls` à l'extérieur des conteneurs.
- **Valve Unidirectionnelle** : Envoi des logs vers `db-log` sans accès direct depuis le conteneur utilisateur.
- **Merkle Ledger (RFC 3161)** : Arbre de Merkle garantissant l'immuabilité et l'horodatage cryptographique infalsifiable.

---

### 🧠 LLM Hors-Ligne & Cartographie STIX 2.1
- **Inférence Offline** : Inférence locale sans aucun accès Internet sortant.
- **Format STIX 2.1 Modulaire (4 Cybercards)** :
  1. `cybercard_attaque` (Indicateurs, vecteurs)
  2. `cybercard_actifs` (Fichiers, processus affectés)
  3. `cybercard_securite` (Mesures actives lors de l'impact)
  4. `cybercard_recommandation` (Vaccins & actions correctives)
- **Signature SHA256** : Signé cryptographiquement par le Bateau MODELE (`signed_by: BATEAU_MODELE_LLM_MASTER`).

---

### 🛡️ Bateau SCIENCE, Bateau TEST & Pipeline de Qualification de Vaccins
- **Base Vectorielle Qdrant** : Indexation et recherche de similarités des menaces.
- **Pipeline de Qualification Formelle (Bateau TEST)** :
  - Analyse syntaxique AST Python (vérification de la structure du code).
  - Analyse de sécurité Bandit Scanner (interdiction de `eval`, `exec`, `os.system`).
  - Mesures d'impact de performance (CPU < 2.0%, RAM < 10 Mo).
  - Rollback automatique en cas d'anomalie post-déploiement (CPU > 85%, taux d'erreur > 5%).

---

### 🔐 Pont Multi-Entreprises & ZKP vers VPS LAB (OBIEY Christ Dany)
- **Anonymisation ZKP (Zero-Knowledge Proofs)** : Nettoyage strict des IP/usernames/fichiers confidentiels avant envoi au LAB.
- **SLA & Diffusion** : Propagation des vaccins qualifiés entre le LAB Central et les VPS Clients.

---

## 2. 🧪 TOUTES LES COMMANDES DE TESTS ET LEUR DESCRIPTION

### 2.1 Lancement Global de la Suite de Tests

```bash
# Lancer tous les tests unitaires, d'intégration, d'audit et de non-régression
PYTHONPATH=. pytest

# Lancer la suite de tests avec un niveau de détail verbeux
PYTHONPATH=. pytest -v

# Lancer un fichier de test spécifique
PYTHONPATH=. pytest tests/test_niveau1_iam.py -v
```

---

### 2.2 Description des Fichiers de Tests dans `tests/`

| Fichier de Test (`tests/`) | Nombre de Tests | Description du Domaine Traité | Statut |
| :--- | :---: | :--- | :---: |
| `tests/test_niveau1_iam.py` | 3 | Contrôle d'accès TPM 2.0, SSH Proxy, stabilité sous charge nominale (10k req/s), isolation des namespaces et cgroups v2. | **PASSED** |
| `tests/test_niveau2_quarantine.py` | 4 | Routage de déception (`mike-vrai` vs `mike-faux`), étanchéité eBPF Cilium, sidecar Falco, canary tokens et détection d'évasion sandbox. | **PASSED** |
| `tests/test_niveau3_llm_stix.py` | 3 | Souveraineté du LLM local hors-ligne, génération des 4 Cybercards STIX 2.1, assainissement eBPF anti-injection de prompt. | **PASSED** |
| `tests/test_niveau4_vector_vaccine.py` | 3 | Moteur vectoriel Qdrant, recherche de similarités, synthèse et déduplication des vaccins de sécurité. | **PASSED** |
| `tests/test_niveau5_qualifier.py` | 4 | Qualification formelle AST Python, scanner de sécurité Bandit (0 faille autorisée), rollback automatique post-anomalie. | **PASSED** |
| `tests/test_niveau6_vps_zkp.py` | 3 | Anonymisation Zero-Knowledge Proofs (ZKP), propagation des vaccins multi-entreprises, résilience du pipeline GitOps gRPC. | **PASSED** |
| `tests/test_niveau7_ha_compliance.py` | 2 | Bascule Haute Disponibilité (HA Hot-Standby < 2s), conformité réglementaire (OHADA, Malabo, ISO 27001) et auditabilité. | **PASSED** |
| `tests/test_roadmap_architecture.py` | 3 | Validation de l'architecture d'extension (Centre IA STIX, Lab Qdrant, Cloud Souverain Systalink). | **PASSED** |
| `tests/test_structure_and_cli.py` | 6 | Conformité de l'arborescence, validation des règles YAML Falco, CLI `cybersocle.cli` (modes `--client` et `--lab`) et qualifier. | **PASSED** |
| `tests/test_api_security.py` | 7 | Audit de sécurité FastAPI, authentification par clé API Bearer, protection contre le Rate-Limiting et injection SQL/Commandes. | **PASSED** |
| `tests/test_cybersocle.py` | 24 | Tests unitaires complets des modules internes `cybersocle/` (auth, network, isolation, logging, llm, science, ecosystem, web). | **PASSED** |
| `tests/test_security_audit.py` | 4 | Analyseur statique de sécurité du code (`SecurityAuditor`), calcul de score de sécurité et détection d'anti-patterns. | **PASSED** |
| `tests/test_finetune_cybersocle.py` | 3 | Pipeline de fine-tuning LoRA/QLoRA DeepSeek-Coder, masquage de données anonymisées et préparation des datasets. | **PASSED** |
| `tests/test_non_regression.py` | 2 | Tests de non-régression sur le modèle de langage et les prompts de sécurité. | **PASSED** |
| `tests/test_templates.py` | 2 | Validation du format de gabarit d'instructions et des jetons EOT/FIM. | **PASSED** |
| `tests/test_tokenizer.py` | 2 | Alignement du vocabulaire, vérification des jetons spéciaux du tokenizer DeepSeek-Coder. | **PASSED** |

---

### 2.3 Commandes CLI Directes de Test & Validation

```bash
# 1. Tester le déploiement CLI en mode Client
python -m cybersocle.cli --client

# 2. Tester le déploiement CLI en mode LAB (OBIEY Christ Dany)
python -m cybersocle.cli --lab

# 3. Exécuter le test de qualification formelle de vaccin
python -m cybersocle.science.qualifier --vaccine-id VACC-2026-001

# 4. Vérifier la syntaxe du fichier de règles Falco eBPF
python -c "import yaml; data=yaml.safe_load(open('cybersocle/isolation/rules.yaml')); print('Règles Falco valides:', len(data))"
```

---

## 3. 🏢 DÉPLOIEMENT SUR LE VPS CLIENT (LLM LOCAL TRÈS LÉGER <= 8 GB RAM)

Le VPS Client est le serveur d'infrastructure déployé chez l'entreprise cliente. Il exécute les 5 Bateaux locaux, la déception SSH et le moteur LLM local pour la génération de cartographies STIX 2.1.

### 📊 Allocation Budgétaire de la Mémoire RAM (Budget Total = 8 GB)
- **Système d'Exploitation & Démons Linux (Kernel, Systemd, SSH)** : ~1.2 GB
- **Démon Docker Engine & Conteneurs (OFFICIEL, PRISON, Falco, Sidecars)** : ~1.8 GB
- **Base Vectorielle Qdrant & Moteur Python SCIENCE** : ~1.0 GB
- **Modèle LLM Local Hors-Ligne (Bateau MODELE)** : **3.0 GB à 3.8 GB MAX**
- **Marge de Sécurité / Buffer CPU/RAM** : ~0.5 GB à 1.0 GB

---

### 🤖 Choix du Modèle LLM pour le VPS Client (8 GB RAM Max)
- **Modèle sélectionné** : **Qwen2.5-Coder-3B-Instruct** (ou **Phi-3-mini-4k-instruct**)
- **Format & Quantification** : **GGUF Q4_K_M (4-bit)**
- **Poids du fichier sur disque** : ~2.0 GB
- **Empreinte VRAM / RAM lors de l'inférence** : **~2.8 GB à 3.2 GB RAM**
- **Performance d'Inférence CPU/RAM** : ~25 - 40 tokens/sec sur 4 vCPUs.

---

### 🛠️ Commandes de Déploiement étape par étape chez le VPS Client

```bash
# 1. Préparer l'environnement et le répertoire des modèles
mkdir -p ./models

# 2. Télécharger le modèle LLM ultra-optimisé Qwen2.5-Coder-3B-Instruct (Quantifié Q4_K_M)
curl -L -o ./models/qwen2.5-coder-3b-q4.gguf \
  "https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct-GGUF/resolve/main/qwen2.5-coder-3b-instruct-q4_k_m.gguf"

# 3. Initialiser les 5 Bateaux et la micro-segmentation eBPF via la CLI CYBERSOCLE
python -m cybersocle.cli --client

# 4. Lancer la pile Docker durcie (Bateau MODELE configuré avec 8GB RAM profile)
docker compose -f docker-compose.yml up -d --build

# 5. Tester l'inférence du LLM local hors-ligne sur le Bateau MODELE
python -c "
from cybersocle.llm.offline_engine import OfflineLLMEngine
engine = OfflineLLMEngine(model_path='./models/qwen2.5-coder-3b-q4.gguf', profile='FULL_CLUSTER')
print(engine.query_model_offline('Analyse de la tentative d intrusion SSH sur mike-faux'))
"
```

---

## 4. 🧪 DÉPLOIEMENT SUR LE VPS LAB (LLM LOCAL TRÈS LÉGER <= 2 GB RAM)

Le VPS LAB est l'infrastructure centrale dirigée par **OBIEY Christ Dany**. Il fait office de hub central de réception des cartographies ZKP, de validation globale des vaccins et de synchronisation multi-entreprises. Pour maintenir un coût d'exploitation minimal, il doit tourner sur un VPS très contraint avec **2 GB RAM maximum**.

### 📊 Allocation Budgétaire de la Mémoire RAM (Budget Total = 2 GB)
- **Système d'Exploitation Linux Alpin / Debian Minimal & Kernel** : ~350 MB
- **Démon Containerd / Docker Minimal Rootless** : ~250 MB
- **Moteur ZKP Anonymizer & Hub Multi-Entreprises CYBERSOCLE** : ~200 MB
- **Modèle LLM Local Ultra-Léger (Bateau MODELE LAB)** : **~800 MB à 1000 MB MAX**
- **Buffer / Marge système** : ~200 MB

---

### 🤖 Choix du Modèle LLM pour le VPS LAB (2 GB RAM Max)
- **Modèle sélectionné** : **Qwen2.5-Coder-0.5B-Instruct** (ou **SmolLM2-360M-Instruct**)
- **Format & Quantification** : **GGUF Q4_K_M (4-bit)**
- **Poids du fichier sur disque** : ~390 MB
- **Empreinte RAM en exécution** : **~450 MB à 650 MB RAM**
- **Performance d'Inférence CPU/RAM** : ~50 - 80 tokens/sec sur 2 vCPUs.

---

### 🛠️ Commandes de Déploiement étape par étape chez le VPS LAB

```bash
# 1. Créer le dossier des modèles sur le VPS LAB
mkdir -p ./models

# 2. Télécharger le modèle LLM ultra-léger Qwen2.5-Coder-0.5B-Instruct (Quantifié Q4_K_M)
curl -L -o ./models/qwen2.5-coder-0.5b-q4.gguf \
  "https://huggingface.co/Qwen/Qwen2.5-Coder-0.5B-Instruct-GGUF/resolve/main/qwen2.5-coder-0.5b-instruct-q4_k_m.gguf"

# 3. Initialiser la pile LAB Central via la CLI CYBERSOCLE (OBIEY Christ Dany)
python -m cybersocle.cli --lab

# 4. Configurer le profil EDGE ultra-léger du moteur LLM offline pour le Bateau MODELE LAB
python -c "
from cybersocle.llm.offline_engine import OfflineLLMEngine
engine = OfflineLLMEngine(model_path='./models/qwen2.5-coder-0.5b-q4.gguf', profile='EDGE')
cfg = engine.get_hardware_resource_config()
print('Configuration Matérielle LAB VPS (2 GB Max):', cfg)
"

# 5. Démarrer le serveur d'inférence C++ ultra-léger llama-server (empreinte < 600 Mo RAM)
llama-server \
  --model ./models/qwen2.5-coder-0.5b-q4.gguf \
  --ctx-size 1024 \
  --threads 2 \
  --batch-size 1 \
  --port 8080 \
  --host 127.0.0.1 &
```

---

## 5. ⚡ COMMANDES POUR DÉPLOYER TOUTE LA PUISSANCE DU LLM PAR POIDS ET TYPE DE VPS

Pour tirer le maximum de performance et de qualité de réponse tout en respectant scrupuleusement les contraintes de mémoire RAM de chaque machine, voici les commandes de déploiement d'inférence par moteur et par poids.

### 5.1 Option A : Déploiement via Ollama (Recommandé pour sa simplicité)

```bash
# === SUR LE VPS LAB (2 GB RAM MAX - Modèle 0.5B) ===
# 1. Installer Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Lancer le modèle 0.5B ultra-léger en imposant la limite de contexte
OLLAMA_NUM_PARALLEL=1 OLLAMA_MAX_LOADED_MODELS=1 ollama run qwen2.5-coder:0.5b

# === SUR LE VPS CLIENT (8 GB RAM MAX - Modèle 3B / 7B) ===
# 1. Lancer le modèle 3B optimisé
OLLAMA_NUM_PARALLEL=2 OLLAMA_MAX_LOADED_MODELS=1 ollama run qwen2.5-coder:3b
```

---

### 5.2 Option B : Déploiement via `llama.cpp` / `llama-server` (Inférence C++ ultra-optimisée)

```bash
# === SERVEUR LAB (VPS LAB 2 GB RAM - Qwen2.5-Coder 0.5B Q4_K_M) ===
llama-server \
  --model ./models/qwen2.5-coder-0.5b-q4.gguf \
  --alias "cybersocle-lab-llm" \
  --ctx-size 1024 \
  --n-predict 512 \
  --threads 2 \
  --batch-size 4 \
  --mlock \
  --host 172.28.0.30 \
  --port 8000

# === SERVEUR CLIENT (VPS CLIENT 8 GB RAM - Qwen2.5-Coder 3B Q4_K_M) ===
llama-server \
  --model ./models/qwen2.5-coder-3b-q4.gguf \
  --alias "cybersocle-client-llm" \
  --ctx-size 2048 \
  --n-predict 1024 \
  --threads 4 \
  --batch-size 16 \
  --mlock \
  --host 172.28.0.30 \
  --port 8000
```

---

## 6. 📊 TABLEAU COMPARATIF DES CARACTÉRISTIQUES, MODÈLES, POIDS, RAM, RÔLES ET VERSIONS

| Critère / Caractéristique | 🧪 VPS LAB Central (OBIEY Christ Dany) | 🏢 VPS Client (Entreprise Cliente) |
| :--- | :--- | :--- |
| **Limite RAM Maximale** | **2 GB RAM Maximum** | **8 GB RAM Maximum** |
| **Ressources CPU Cibles** | 1 à 2 vCPUs (ex. KVM / Cloud VPS Start) | 2 à 4 vCPUs (ex. Cloud VPS Medium) |
| **Stockage NVMe Requis** | 20 Go NVMe SSD | 50 Go à 100 Go NVMe SSD |
| **Système & Noyau Requis** | Linux Ubuntu 22.04 LTS / Debian 12 (Noyau 5.15+) | Linux Ubuntu 22.04 LTS / Debian 12 (Noyau 5.15+) |
| **Modèle LLM Recommandé** | **Qwen2.5-Coder-0.5B-Instruct** (ou SmolLM2-360M) | **Qwen2.5-Coder-3B-Instruct** (ou DeepSeek-Coder-1.3B/6.7B) |
| **Format & Quantification** | GGUF Q4_K_M (4-bit) | GGUF Q4_K_M (4-bit) |
| **Poids Fichier Modèle (Disque)**| **~390 Mo** | **~2.0 Go** |
| **Consommation RAM du LLM** | **~450 Mo à 650 Mo RAM** | **~2.8 Go à 3.2 Go RAM** |
| **Vitesse d'Inférence (Tokens/s)**| ~50 à 80 tokens/sec | ~25 à 45 tokens/sec |
| **Version CYBERSOCLE** | **v1.0.0** (`python -m cybersocle.cli --lab`) | **v1.0.0** (`python -m cybersocle.cli --client`) |
| **Version Python** | **Python 3.11 / 3.12** | **Python 3.11 / 3.12** |
| **Moteur d'Inférence C++** | `llama.cpp` / `llama-server` (b3000+) | `vLLM` / `llama.cpp` (b3000+) |
| **Profil Moteur (`offline_engine`)**| `EDGE` (`vram_limit_mb: 2048`, `batch_size: 1`) | `FULL_CLUSTER` (`vram_limit_mb: 8192`, `batch_size: 16`) |
| **Rôle Principal dans CYBERSOCLE**| Concentrateur ZKP, validation globale des vaccins, synchronisation inter-entreprises. | Protection locale 5 Bateaux, déception SSH, cartographie STIX 2.1 locale. |

---

## 7. 🪟 EXÉCUTION SOUS WINDOWS TOUT EN GARDANT SON NOYAU LINUX POUR LES TESTS

Pour faire tourner CYBERSOCLE et exécuter l'intégralité de la suite de tests sur une machine hôte **Windows** tout en conservant le **noyau Linux sous-jacent** indispensable aux fonctionnalités de sécurité avancées (eBPF Cilium, Falco syscall tracing, cgroups v2, namespaces, iptables), le projet s'appuie sur la technologie **WSL2 (Windows Subsystem for Linux v2)** et le **Docker Desktop Linux Backend**.

### 7.1 Architecture d'Exécution Sous Windows

```
+-------------------------------------------------------------------------+
|                        HÔTE WINDOWS 10 / 11                             |
+-------------------------------------------------------------------------+
|   WSL2 (Windows Subsystem for Linux) - Kernel Linux 5.15+ / 6.x réel    |
|   +-----------------------------------------------------------------+   |
|   |   Docker Desktop Engine (Linux Containers Backend)              |   |
|   |   +---------------------------------------------------------+   |   |
|   |   |   CYBERSOCLE Stack (5 Bateaux)                            |   |   |
|   |   |   - eBPF / Cilium Network Filtering (Noyau Linux)       |   |   |
|   |   |   - Sidecar Falco Syscall Tracing                       |   |   |
|   |   |   - Namespaces & Cgroups v2                             |   |   |
|   |   |   - Pytest Test Suite (75/75 Tests Passed)              |   |   |
|   |   +---------------------------------------------------------+   |   |
|   +-----------------------------------------------------------------+   |
+-------------------------------------------------------------------------+
```

---

### 7.2 Étapes de Configuration sous Windows (PowerShell / WSL2)

#### Étape 1 : Activer WSL2 avec un noyau Linux Ubuntu
Dans un terminal PowerShell sous Windows (en mode Administrateur) :

```powershell
# Activer WSL et installer la distribution Ubuntu avec noyau Linux 5.15+
wsl --install -d Ubuntu-22.04

# S'assurer que la version WSL par défaut est WSL2
wsl --set-default-version 2
```

#### Étape 2 : Lancer l'environnement Linux sous Windows
Ouvrir le terminal WSL2 Ubuntu :

```bash
# Se placer dans l'environnement WSL2
wsl -d Ubuntu-22.04

# Naviguer vers le répertoire du projet CYBERSOCLE
cd /mnt/c/Users/VotreNom/Projets/cybersocle
```

#### Étape 3 : Exécuter la suite complète de tests Linux sous Windows
Dans le terminal WSL2 Ubuntu :

```bash
# 1. Vérifier la version du noyau Linux sous-jacent sous Windows
uname -r
# Output attendu : 5.15.x-microsoft-standard-WSL2 (Noyau Linux authentique)

# 2. Installer les dépendances Python dans l'environnement WSL2
pip install -e .
pip install pyyaml pydantic fastapi pytest

# 3. Lancer la totalité des 75 tests de CYBERSOCLE sous Windows (via Noyau Linux WSL2)
PYTHONPATH=. pytest
```

---

### 7.3 Prise en Charge Inter-Plateformes dans le Code Python (`cybersocle`)

Les modules Python du projet CYBERSOCLE intègrent des mécanismes de fallback pour garantir que les scripts d'administration et de tests fonctionnent sans crash même lorsqu'ils sont exécutés dans un environnement Windows natif hors-WSL (en simulant les binaires `falco` ou `cilium`) :

```python
import sys
import subprocess

def run_kernel_check():
    """
    Détecte l'environnement d'exécution et adapte les vérifications noyau.
    """
    is_windows = sys.platform.startswith("win")
    if is_windows:
        print("[CYBERSOCLE] Exécution sous Windows. Recommandation : Utilisez WSL2 avec Noyau Linux pour eBPF.")
    else:
        print("[CYBERSOCLE] Exécution sous Noyau Linux natif. eBPF et Falco pleinement actifs.")
```

Grâce à cette approche, **CYBERSOCLE conserve 100% de sa puissance eBPF/Linux** tout en offrant une expérience de développement et de test fluide sur Windows.
