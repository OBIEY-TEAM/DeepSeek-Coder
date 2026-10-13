# DIRECTIVES DE REFACTORISATION DU PROJET CYBERSOCLE

Ce document contient la spécification complète, rigoureuse et détaillée pour assainir le dépôt de code, éliminer l'ensemble des résidus de l'ancien modèle/dépôt amont (DeepSeek Coder), et restructurer le projet afin d'obtenir une base de code 100 % dédiée à **CYBERSOCLE**.

---

## 1. DIAGNOSTIC ET ANALYSE DE L'ETAT ACTUEL DU PROJET

Après une analyse exhaustive de la totalité des fichiers du dépôt, la structure se divise en deux catégories :

### A. Composants natifs et légitimes CYBERSOCLE (À CONSERVER ET STRUCTURER)
1. **Core Package (`cybersocle/`)** :
   - `cybersocle/auth/` : Isolation navigateur (`browser_isolation.py`), leurres dynamiques SSH (`decoy_generator.py`), proxy SSH (`ssh_proxy.py`), attestation matérielle (`tpm_attestation.py`).
   - `cybersocle/network/` : Microsegmentation eBPF/Cilium (`ebpf_cilium.py`), gestionnaire VLAN (`vlan_manager.py`), durcissement conteneurs (`container_hardening.py`).
   - `cybersocle/logging/` : Journalisation Merkle Ledger immuable (`merkle_ledger.py`), sidecar Falco (`sidecar_falco.py`), tuyau unidirectionnel (`unidirectional_pipe.py`).
   - `cybersocle/isolation/` : Moteur d'isolation et de quarantaine d'incidents (`incident_manager.py`), règles d'isolation (`rules.yaml`).
   - `cybersocle/llm/` : Moteur IA local offline (`offline_engine.py`), cybercartographie STIX 2.1 (`stix_cybercards.py`).
   - `cybersocle/science/` : Moteur de vaccins cyber (`vaccine_engine.py`, `vaccine_validation.py`), qualification des menaces (`qualifier.py`), lab vectoriel (`vector_lab.py`).
   - `cybersocle/ecosystem/` : Multi-entreprises (`multi_enterprise.py`), GitOps manager (`gitops_manager.py`).
   - `cybersocle/web/` : Backend API (`api_backend.py`), Interface utilisateur (`ui_app.py`).
   - `cybersocle/cli.py` & `cybersocle/__init__.py` : Point d'entrée en ligne de commande.

2. **Démonstration & Interface Web (`demo/`)** :
   - `demo/app.py`, `demo/style.css`, `demo/requirement.txt`.

3. **Infrastructures, Serveurs & Entraînement (`serve/`, `finetune/`, `devops/`)** :
   - `serve/api_server.py`, `serve/security_audit.py`, `serve/vllm_server.py`.
   - `finetune/finetune_cybersocle.py`, `finetune/merge_peft_adapters.py`, `finetune/configs/ds_config_zero3.json`, `finetune/requirements.txt`, `finetune/README.md`.
   - `devops/devops.md` : Guide complet de déploiement VPS Client / VPS Lab, contraintes mémoire, WSL2.

4. **Banc de Tests (`tests/`)** :
   - Tous les fichiers de tests Python (`test_api_security.py`, `test_cybersocle.py`, `test_finetune_cybersocle.py`, `test_niveau1_iam.py`, `test_niveau2_quarantine.py`, `test_niveau3_llm_stix.py`, `test_niveau4_vector_vaccine.py`, `test_niveau5_qualifier.py`, `test_niveau6_vps_zkp.py`, `test_niveau7_ha_compliance.py`, `test_non_regression.py`, `test_roadmap_architecture.py`, `test_security_audit.py`, `test_structure_and_cli.py`, `test_templates.py`, `test_tokenizer.py`).

5. **Documentation Institutionnelle et Légale** :
   - `DOCS_CYBERSOCLE.md`, `SUPPORT.md`, `SECURITY.md`, `SECURITY_AUDIT_REPORT.md`, `INCIDENT_RESPONSE.md`, `DISASTER_RECOVERY.md`, `COMPLIANCE.md`, `SLA.md`, `ETHICS.md`, `PRIVACY.md`, `TERMS.md`, `DATASHEET.md`, `MODEL_CARD.md`, `ROADMAP.md`, `FAQ.md`, `TROUBLESHOOTING.md`, `PERFORMANCE.md`, `ACKNOWLEDGMENTS.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SBOM.json`.

6. **Images de Marque et Captures CYBERSOCLE (`pictures/`)** :
   - `pictures/logo.png`, `pictures/logo.jpeg`, `pictures/home.png`, `pictures/home.tif`.

---

### B. Eléments obsolètes, hors-sujet ou résiduels à supprimer
1. **Le dossier de benchmarks `Evaluation/` dans sa totalité** :
   - `Evaluation/DS-1000/`
   - `Evaluation/HumanEval/`
   - `Evaluation/LeetCode/`
   - `Evaluation/MBPP/`
   - `Evaluation/PAL-Math/`
   *Raison* : Ce dossier contient des métriques et des jeux de tests de codage générique (LeetCode, Math, MBPP, HumanEval) issus du dépôt de base DeepSeek Coder. Il n'a aucun rapport avec la cybersécurité ou CYBERSOCLE.

2. **Le script d'entraînement obsolète dans `finetune/`** :
   - `finetune/finetune_deepseekcoder.py`
   *Raison* : Remplacé et supplanté par `finetune/finetune_cybersocle.py` adapté à la spécificité des données de cyberdéfense et au masquage d'anonymisation.

3. **Les visuels et graphiques de benchmarks de code dans `pictures/`** :
   - `pictures/DS-1000.png`
   - `pictures/HumanEval.png`
   - `pictures/MBPP.png`
   - `pictures/MPBB.png`
   - `pictures/Math.png`
   - `pictures/completion_demo.gif`
   - `pictures/data_clean.png`
   - `pictures/model_pretraining.png`
   - `pictures/result.png`
   - `pictures/table.png`
   *Raison* : Ces illustrations sont relatives aux scores globaux de génération de code de DeepSeek Coder et polluent le projet CYBERSOCLE.

4. **Les documents markdown résiduels/brouillons dans `tests/`** :
   - `tests/test.md`
   - `tests/test2.md`
   *Raison* : Fichiers texte résiduels inutiles.

5. **Artefacts de build temporaires** :
   - `cybersocle.egg-info/`
   - Fichiers compilés `*.pyc` et dossiers `__pycache__/`.

---

## 2. COMMANDES D'ASSANISSEMENT ET DE SUPPRESSION DETAILLEES

Pour exécuter le nettoyage intégral du projet, exécuter les instructions suivantes :

```bash
# 1. Suppression du dossier complet de benchmarks de code non-CYBERSOCLE
rm -rf Evaluation/

# 2. Suppression du script de fine-tuning générique DeepSeek
rm -f finetune/finetune_deepseekcoder.py

# 3. Nettoyage du dossier pictures/ (suppression des graphiques de benchmarks DeepSeek)
rm -f pictures/DS-1000.png \
      pictures/HumanEval.png \
      pictures/MBPP.png \
      pictures/MPBB.png \
      pictures/Math.png \
      pictures/completion_demo.gif \
      pictures/data_clean.png \
      pictures/model_pretraining.png \
      pictures/result.png \
      pictures/table.png

# 4. Suppression des fichiers de brouillon dans tests/
rm -f tests/test.md tests/test2.md

# 5. Nettoyage des artefacts de build et caches
rm -rf cybersocle.egg-info
find . -type d -name "__pycache__" -exec rm -rf {} +
```

---

## 3. SPECIFICATION DE REECRITURE INTEGRALE DU README.MD

Le fichier `README.md` actuel est principalement le README originel de DeepSeek Coder. Il doit être entièrement réécrit pour présenter **CYBERSOCLE** avec professionnalisme et clarté.

Voici le contenu exact à inscrire dans `README.md` :

```markdown
<p align="center">
  <img src="pictures/logo.png" alt="CYBERSOCLE Logo" width="220px"/>
</p>

<h1 align="center">CYBERSOCLE</h1>

<p align="center">
  <strong>Plateforme Souveraine de Microsegmentation Réseau, Deception SSH & Cybercartographie par IA Offline STIX 2.1</strong>
</p>

<p align="center">
  <a href="https://cybersocle.studio"><img src="https://img.shields.io/badge/Site_Officiel-cybersocle.studio-0052CC?style=for-the-badge&logo=internet-explorer" alt="CYBERSOCLE Studio"/></a>
  <a href="https://wa.me/242066130118"><img src="https://img.shields.io/badge/WhatsApp-Support-25D366?style=for-the-badge&logo=whatsapp" alt="WhatsApp Support"/></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python Version"/>
  <img src="https://img.shields.io/badge/Licence-MIT-green?style=for-the-badge" alt="License"/>
</p>

---

## 🛡️ Présentation

**CYBERSOCLE** est une solution complète de cyberdéfense souveraine et de microsegmentation réseau conçue pour isoler les menaces, détecter les intrusions via déception dynamique et cartographier les incidents en temps réel grâce à un moteur d'IA offline autonome sans dépendance cloud externe.

Conçu pour fonctionner dans des environnements à ressources contraintes (VPS Client avec max 8 GB RAM ou VPS Central LAB avec 2 GB RAM), **CYBERSOCLE** combine l'observabilité réseau eBPF/Falco, la journalisation immuable par Registre Merkle et la génération automatique de vaccins cyber.

<p align="center">
  <img src="pictures/home.png" alt="Interface CYBERSOCLE" width="85%"/>
</p>

---

## ✨ Fonctionnalités Clés

- 🔒 **Microsegmentation Réseau & eBPF Cilium** : Isolement dynamique des flux, conteneurs durcis et VLANs virtuels sécurisés (`cybersocle.network`).
- 🍯 **Proxy SSH Honeypot & Deception** : Piège SSH interactif, leurres dynamiques avec attestation TPM et isolation navigateur (`cybersocle.auth`).
- 📜 **Journalisation Immuable & Sidecar Falco** : Ledger Merkle cryptographique et tuyau unidirectionnel à haute sécurité (`cybersocle.logging`).
- 🤖 **Cartographie Cyber IA Offline & STIX 2.1** : Génération de fiches d'incidents normalisées STIX 2.1 avec LLM local quantifié (`cybersocle.llm`).
- 🧪 **Laboratoire Vectoriel & Vaccin Cyber** : Qualification automatisée des menaces et déploiement de règles de défense (`cybersocle.science`).
- 🚨 **Isolation & Quarantaine d'Incidents** : Clonage d'incidents et application de règles YAML d'urgence (`cybersocle.isolation`).
- 🌐 **Architecture Multi-Entreprises & GitOps** : Gestion multi-tenant et synchronisation des politiques réseau (`cybersocle.ecosystem`).

---

## 🏗️ Architecture des Modules

```
cybersocle/
├── auth/         # Proxies SSH, leurres TPM, isolation navigateur
├── network/      # Microsegmentation eBPF, Cilium, durcissement conteneurs
├── logging/      # Registre immuable Merkle, sidecar Falco, tuyau unidirectionnel
├── isolation/    # Quarantaine d'incidents, gestionnaire de crises & règles YAML
├── llm/          # Moteur LLM local offline, générateur de fiches STIX 2.1
├── science/      # Moteur de vaccins cyber, qualificateur de menaces, lab vectoriel
├── ecosystem/    # Multi-tenant, GitOps & orchestration
├── web/          # Backend API & démonstrateur Gradio
└── cli.py        # Point d'entrée CLI unifié
```

---

## 🚀 Installation & Démarrage Rapide

### 1. Prérequis & Installation

```bash
git clone https://github.com/cybersocle/cybersocle.git
cd cybersocle
pip install -e .
```

### 2. Utilisation de la Ligne de Commande (CLI)

CYBERSOCLE propose deux modes de déploiement optimisés :

- **Mode Client VPS (8 GB RAM)** :
  ```bash
  python -m cybersocle.cli --client
  ```

- **Mode Central LAB VPS (2 GB RAM)** :
  ```bash
  python -m cybersocle.cli --lab
  ```

---

## 🖥️ Démonstration Web & Serveurs API

### Interface Démo Interactive (Gradio)
Consultez l'interface de démonstration bilingue (Français/Anglais) :
```bash
python demo/app.py
```

### Serveur API FastAPI & vLLM
Lancer le serveur API de cyberdéfense :
```bash
python -m serve.api_server
```

Déploiement Docker Compose :
```bash
docker compose up --build -d
```

---

## ⚙️ Fine-Tuning Spécifique CYBERSOCLE

Pour réentraîner le modèle LLM local sur des données de cyberdéfense avec anonymisation intégrée :

```bash
python finetune/finetune_cybersocle.py \
    --data_path ./data/raw_data.json \
    --output_dir ./models/cybersocle-lora
```

---

## 📚 Governance, Documentation & Support

- **Documentation Technique** : `DOCS_CYBERSOCLE.md` & `devops/devops.md`
- **Réponse aux Incidents** : `INCIDENT_RESPONSE.md` & `DISASTER_RECOVERY.md`
- **Sécurité & Conduite** : `SECURITY.md` | `CODE_OF_CONDUCT.md` | `ETHICS.md`
- **Rapports d'Audit** : `SECURITY_AUDIT_REPORT.md` | `COMPLIANCE.md` | `SLA.md`
- **Support Officiel** :
  - **Site Web** : [https://cybersocle.studio](https://cybersocle.studio)
  - **WhatsApp** : [+242 06 613 01 18](https://wa.me/242066130118)

---

## 📄 Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE-CODE](LICENSE-CODE) pour plus de détails.
```

---

## 4. VERIFICATION DE LA CONFORMITE ET TESTS DU PROJET

Une fois l'assainissement et la réécriture effectués, la conformité de CYBERSOCLE doit être validée par les étapes suivantes :

1. Exécution de la suite de tests complète :
   ```bash
   python3 -m pytest tests/
   ```
2. Vérification du CLI CYBERSOCLE :
   ```bash
   python -m cybersocle.cli --help
   ```
3. Lancement de l'interface démo :
   ```bash
   python demo/app.py --help
   ```
