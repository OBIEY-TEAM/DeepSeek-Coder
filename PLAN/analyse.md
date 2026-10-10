# ANALYSE DÉTAILLÉE GÉNÉRALISÉE ET GUIDE DE DÉPLOIEMENT DE CYBERSOCLE

---

## 1. RÉSUMÉ EXÉCUTIF ET PHILOSOPHIE DU SYSTÈME

**CYBERSOCLE** est une plateforme industrielle hybride de cyber-sécurité et de cyber-cartographie autonome. Elle combine la micro-segmentation réseau au niveau du noyau Linux (eBPF Cilium), la conteneurisation immuable et durcie (Namespaces, Cgroups v2, Seccomp, Rootless Docker, MicroVMs Firecracker), une passerelle d'authentification SSH dynamique à leurres (deception engine), un système d'EDR embarqué en sidecar (Falco eBPF), un registre de preuve immuable (Arbre de Merkle avec horodatage RFC 3161), une intelligence artificielle locale hors-ligne (LLM vLLM / GGUF quantifié), la norme internationale de renseignement sur les menaces **STIX 2.1**, un laboratoire d'analyse vectorielle (Qdrant), un moteur de qualification formelle de vaccins (AST, Bandit, métriques de charge), une interface de validation humaine React/FastAPI, et un écosystème multi-entreprises à preuves à connaissance nulle (ZKP) relié au VPS LAB CYBERSOCLE (dirigé par OBIEY Christ Dany).

### L'Analogie des 5 Bateaux
L'architecture de CYBERSOCLE repose sur une abstraction en **5 Bateaux (Enclaves Docker isolées)** déployés sur chaque nœud d'infrastructure (VPS Client et VPS LAB) :

```
+-----------------------------------------------------------------------------------+
|                                  RÉSEAU PRIVÉ                                     |
|                       (reseau-prive: internal=true, eBPF Cilium)                 |
|                                                                                   |
|   +-------------------+    +-------------------+    +-------------------------+   |
|   | 1. BATEAU OFFICIEL|    | 2. BATEAU PRISON  |    | 3. BATEAU MODELE        |   |
|   | (Prod Cells / VPN)|    | (Honeypot / Clones|    | (LLM Offline / ReadOnly)|   |
|   |   mike-vrai       |    |   mike-faux       |    |                         |   |
|   +---------+---------+    +---------+---------+    +------------+------------+   |
|             |                        |                       |                    |
|             +-------- Logs ----------+                       | Read-Only DBs      |
|                          |                                   v                    |
|                          v                          +-------------------------+   |
|                 +-----------------+                 | 4. BATEAU SCIENCE       |   |
|                 |  Sidecar Falco  |                 | (Qdrant Threat Intel)   |   |
|                 |  + Merkle Tree  |                 +------------+------------+   |
|                 +-----------------+                              |                |
|                                                                  v                |
|                                                     +-------------------------+   |
|                                                     | 5. BATEAU TEST          |   |
|                                                     | (AST/Bandit Validation) |   |
|                                                     +-------------------------+   |
+-----------------------------------------------------------------------------------+
```

---

## 2. ANALYSE DÉTAILLÉE MODULE PAR MODULE DES COMPOSANTS DE CODE

La base de code de CYBERSOCLE est organisée sous le package Python `cybersocle/` de manière hautement modulaire :

### 2.1 Package `cybersocle/network/` (Micro-segmentation & Durcissement)
- `vlan_manager.py` (`VLANManager`) :
  Gère la configuration du réseau privé Docker `reseau-prive` (`internal: true`, IPAM subnet `172.28.0.0/16`, bridge `enable_icc: false`). Maintient l'adressage IP statique des 5 Bateaux (`172.28.0.10` à `.50`).
- `ebpf_cilium.py` (`CiliumPolicyGenerator`, `apply_ebpf_microsegmentation`) :
  Génère les politiques eBPF Cilium CNI (L3/L4/L7) restreignant le trafic inter-conteneurs. Force le Bateau SCIENCE à ne parler **qu'au Bateau MODELE**, isole les cellules compromises via des politiques de quarantaine eBPF instantanées.
- `container_hardening.py` (`ContainerHardeningProfile`) :
  Fournit la configuration de durcissement des conteneurs : système de fichiers immuable `--read-only`, `tmpfs`, Cgroups v2 (limite 2 GB RAM), profils Seccomp/AppArmor stricts, et option d'exécution en micro-VM Firecracker / Kata Containers.

### 2.2 Package `cybersocle/auth/` (Gateway Proxy SSH & Déception)
- `ssh_proxy.py` (`SSHAuthenticationGateway`, `BehavioralAIAuthAgent`) :
  Contrôle les accès SSH à l'entrée du Bateau OFFICIEL.
  - L'agent IA d'analyse comportementale évalue la cadence de frappe, la vélocité des commandes et les appels système suspects (détection de bots ou de vols de sessions).
  - La passerelle exige un mot de passe, une clé de chiffrement locale valide, l'attestation TPM 2.0 et un comportement sain pour accorder l'identité `mike-vrai` avec accès VPN.
  - En cas de manquement, l'accès est basculé vers `mike-faux` dans le Bateau PRISON (honeypot).
- `decoy_generator.py` (`LLMDecoyDataGenerator`) :
  Génère dynamiquement de faux documents d'entreprise crédibles (bilans comptables, accès serveurs, clés API fictives) enrichis de **Canary Tokens** piégés.
- `tpm_attestation.py` (`HardwareAttestationValidator`) :
  Vérifie les citations PCR et les signatures cryptographiques de puces TPM 2.0 / Secure Enclave pour éliminer les réutilisations non autorisées de clés RSA.
- `browser_isolation.py` (`IsolatedBrowserVPNProxy`) :
  Contrôle le navigateur sécurisé dans la cellule : seul `mike-vrai` dispose du tunnel VPN d'entreprise vers les applications internes.

### 2.3 Package `cybersocle/logging/` (EDR Sidecar & Immuabilité)
- `sidecar_falco.py` (`eBPFFalcoSidecarAgent`) :
  Sidecar espion léger (~20 Mo RAM) exécuté à l'extérieur des cellules pour observer les appels système (`syscalls`) via eBPF. Détecte en temps réel les reverse shells, injections mémoire, et tentatives d'évasion.
- `unidirectional_pipe.py` (`UnidirectionalLogValve`) :
  Tuyau à sens unique empêchant toute cellule compromise d'écrire ou de modifier directement la base de données de logs (`db-log`).
- `merkle_ledger.py` (`MerkleTreeLogLedger`) :
  Structure d'Arbre de Merkle assurant le scellement cryptographique des logs au fil de l'eau avec horodatage RFC 3161 certifié.

### 2.4 Package `cybersocle/llm/` (Inférence & Cybercartographie STIX 2.1)
- `offline_engine.py` (`OfflineLLMMasterEngine`) :
  Exécuteur LLM hors-ligne fonctionnant avec vLLM ou llama.cpp (modèles quantifiés GGUF 4/8-bit). Lit les volumes de bases de données en lecture seule stricte (`--read-only`, `tmpfs`).
- `stix_cybercards.py` (`STIXCybercardGenerator`) :
  Génère des bundles STIX 2.1 structurés en 4 Cybercards (`cybercard_attaque`, `cybercard_actifs`, `cybercard_securite`, `cybercard_recommandation`), signés avec une signature SHA256. Intègre également la fonction d'anonymisation pour le partage avec le LAB.

### 2.5 Package `cybersocle/isolation/` (Incident & Emergency Management)
- `incident_manager.py` (`IncidentIsolationManager`) :
  Gère l'isolation d'urgence des cellules, le clonage vers le Bateau PRISON, la régénération du Bateau OFFICIEL avec forçage de la double authentification (2FA sur 10 reconnexions), la régénération du Bateau PRISON lors d'évasions, et la restauration du Bateau SCIENCE. Contient un garde-fou anti-épuisement de ressources (limite du nombre de clones et débit de clonage).

### 2.6 Package `cybersocle/science/` (Threat-Intel-Lab & Validation de Vaccins)
- `vector_lab.py` (`QdrantThreatIntelLab`) :
  Base vectorielle Qdrant analysant les embeddings des Cybercards STIX 2.1 pour faire ressortir les objectifs de sécurité et les modèles de risques.
- `vaccine_engine.py` (`SecurityVaccineEngine`) :
  Moteur d'apprentissage générant les scripts et patchs de renforcement ("vaccins").
- `vaccine_validation.py` (`FormalVaccineValidator`) :
  Validateur exécutant les contrôles sur le Bateau TEST : analyse syntaxique AST, scanner Bandit, mesure d'overhead CPU/RAM, calcul du score de confiance, auto-approbation ou demande de validation humaine, et réinitialisation snapshot du Bateau TEST.

### 2.7 Package `cybersocle/web/` (Interface Validation Admin)
- `api_backend.py` (`app` FastAPI) & `ui_app.py` (`render_human_validation_dashboard_html`) :
  Dashboard d'administration sécurité accessible via VPN/SSH exécuté dans la cellule `admin-security`. Permet à l'administrateur de consulter les recommandations et d'approuver en 1 clic le déploiement d'un vaccin.

### 2.8 Package `cybersocle/ecosystem/` (Multi-Entreprises & GitOps)
- `multi_enterprise.py` (`MultiEnterpriseLabBridge`, `ZeroKnowledgeProofAnonymizer`) :
  Gestionnaire d'interconnexion VPN entre les bateaux des entreprises clientes et le VPS LAB CYBERSOCLE (OBIEY Christ Dany). Applique les preuves ZKP et l'anonymisation complète.
- `gitops_manager.py` (`GitOpsPolicyManager`) :
  Gestionnaire d'état de sécurité basé sur un dépôt Git local (`.cybersocle_gitops`). Offre un suivi des commits de politiques et permet le rollback instantané (`git revert`).

### 2.9 CLI de Déploiement `cybersocle/cli.py`
Propose l'interface en ligne de commande principale pour déployer la pile globale sur un VPS Client (`--client`) ou sur le VPS LAB (`--lab`).

---

## 3. LIFECYCLE COMPLET : DU DÉCLENCHEMENT DE L'ATTAQUE À LA DISTRIBUTION DU VACCIN

```
[1. Tentative SSH User 'mike']
       |
       +---> [Passerelle SSH & Agent IA Comportemental]
                 |
                 +---> Authentification Conforme (TPM + Clé) -> mike-vrai (OFFICIEL + VPN)
                 |
                 +---> Identifiant / TPM Invalide ou Anomalie -> mike-faux (PRISON Honeypot)
                                                                       |
[2. Exécution d'un Payload / Malware dans la Cellule] <----------------+
       |
       v
[3. Détection eBPF Falco Sidecar] -> Alerte Système
       |
       v
[4. Isolation Réseau eBPF & Merkle Log Ledger] -> Inscription immuable RFC 3161
       |
       v
[5. Clonage de Cellule vers PRISON & Destruction OFFICIEL] -> Session redirigée
       |
       v
[6. Bateau MODELE (LLM Read-Only)] -> Génération Cybercartographie STIX 2.1 (4 Cybercards + Hash SHA256)
       |
       v
[7. Transmis au Bateau SCIENCE (Qdrant Vector Lab)] -> Vectorisation & Moteur de Vaccins
       |
       v
[8. Bateau TEST (Validation Formelle)] -> AST Python + Bandit Scanner + Score de Confiance
       |
       +---> Score >= 0.90 & Criticité Moyenne -> Auto-approbation
       |
       +---> Score < 0.90 ou Criticité Élevée -> Validation Humaine 1-Clic Dashboard React/FastAPI
                                                        |
[9. Application GitOps Commit] <-----------------------+
       |
       v
[10. Anonymisation ZKP & Export vers VPS LAB CYBERSOCLE (OBIEY Christ Dany)]
       |
       v
[11. Validation LAB & Re-distribution globale aux Bateaux SCIENCE des autres clients]
```

---

## 4. GARANTIES DE SÉCURITÉ ET RÉSILIENCE OPÉRATIONNELLE

1. **Étanchéité Zéro-Confiance (Zero Trust)** :
   - Aucun conteneur ne possède de privilèges super-utilisateur.
   - Micro-segmentation eBPF L3/L4/L7 bloquant tout trafic non explicitement autorisé.
   - Reseau privé `reseau-prive` strictement isolé d'Internet (`internal: true`).
2. **Immuabilité & Non-Répudiation des Logs** :
   - Tuyau à sens unique empêchant l'altération de la BDD de logs.
   - Arbre de Merkle scellant les événements avec horodatage RFC 3161.
3. **Isolation Matérielle & Protection Noyau** :
   - Cellules à haut risque exécutées dans des micro-VMs Firecracker (isolation KVM/noyau dédié).
   - Profils Seccomp / AppArmor désactivant les appels système de modification du noyau.
4. **Protections Anti-Déni de Service (DoS)** :
   - Garde-fou anti-épuisement de ressources empêchant le clonage en boucle infinie par un attaquant dans le Bateau PRISON.
5. **Rollback Déterministe (GitOps)** :
   - Traçabilité complète de chaque mise à jour de sécurité via commits Git signés.
   - Rollback immédiat automatique ou manuel en cas d'anomalie post-déploiement.

---

## 5. GUIDE DE DÉPLOIEMENT OPÉRATIONNEL PAS-À-PAS

### 5.1 Prérequis Système

- **OS Recommandé** : Ubuntu Server 22.04 LTS / 24.04 LTS ou Debian 12.
- **Ressources Minimales Recommandées** :
  - **VPS Client** : 4 vCPU, 16 Go RAM, 100 Go NVMe, GPU optionnel (ou CPU AVX-512 pour LLM GGUF).
  - **VPS LAB (OBIEY Christ Dany)** : 8 vCPU, 32 Go RAM, 250 Go NVMe, NVIDIA GPU (RTX 4090 / A10G).
- **Dépendances Logicielles** :
  - Docker Engine >= 24.0 (avec support Rootless activé).
  - Docker Compose v2.
  - Python 3.11 / 3.12.
  - Linux Kernel >= 5.15 (pour le support complet eBPF / Cilium).

### 5.2 Déploiement sur VPS Entreprise Cliente

1. **Cloner le Dépôt & Installer le Package Python** :
   ```bash
   git clone https://github.com/CyberCode-Studio/deepseek-coder-cybercode.git /app
   cd /app
   pip install -e .
   ```

2. **Configurer le Fichier d'Environnement `.env`** :
   ```bash
   cp .env.example .env
   # Définir les clés de sécurité
   echo "CYBERSOCLE_ADMIN_TOKEN=admin-cybersocle-secret-2025" >> .env
   echo "CYBERSOCLE_LAB_VPN_IP=10.100.0.1" >> .env
   ```

3. **Exécuter la Commande de Déploiement CLI Client** :
   ```bash
   python -m cybersocle.cli --client
   ```

4. **Lancer les Services Docker Compose** :
   ```bash
   docker compose up -d --build
   ```

### 5.3 Déploiement sur VPS LAB CYBERSOCLE (OBIEY Christ Dany)

1. **Initialiser l'Environnement sur le VPS LAB Central** :
   ```bash
   cd /app
   pip install -e .
   ```

2. **Exécuter la Commande de Déploiement CLI LAB** :
   ```bash
   python -m cybersocle.cli --lab
   ```

3. **Activer le Concentrateur Multi-Entreprises** :
   Le VPS LAB initialise le pont VPN central, le récepteur de Cybercartographies anonymisées ZKP et le registre global de distribution des vaccins.

### 5.4 Procédure de Vérification & Tests Automatisés

Après tout déploiement ou modification de code, exécuter la suite complet de tests unitaires pour valider le bon fonctionnement de tous les sous-systèmes :

```bash
PYTHONPATH=. pytest tests/test_cybersocle.py
```

Résultat attendu : **24/24 tests validés avec succès**.
