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
