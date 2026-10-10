# PROMPT APLIQUANT LES AMÉLIORATIONS AU PROJET CYBERSOCLE (`PLAN/prompt-amelioration.md`)

Vous êtes l'Architecte Sécurité et Lead Principal du projet **CYBERSOCLE**.
Votre tâche est de mettre à jour et d'élever l'ensemble de l'infrastructure et du code du projet CYBERSOCLE en appliquant l'intégralité des améliorations techniques, sécuritaires et architecturales formalisées dans `PLAN/amelioration.md`.

---

## RÈGLES ET DIRECTIVES D'AMÉLIORATION PAR MODULE

### 1. REHAUSSEMENT SÉCURITÉ RESEAU ET CONTAINERISATION
- **Micro-segmentation eBPF (Cilium CNI)** :
  - Remplacer ou compléter les règles iptables/docker network basiques par des règles de filtrage eBPF strictes au niveau L3/L4/L7. Bloquer tout trafic inter-cellules direct et forcer le passage par le Sidecar et les proxys dédiés.
- **Rootless Docker, AppArmor & Seccomp** :
  - Configurer les daemons et conteneurs pour s'exécuter en mode Rootless.
  - Appliquer les profils Seccomp et AppArmor durcis empêchant les appels système dangereux (`ptrace`, `kexec_load`, `sys_admin`).
- **Kata Containers / Firecracker MicroVMs** :
  - Configurer `containerd` pour exécuter les cellules à risque et les clones du Bateau PRISON dans des micro-VMs isolées par hyperviseur (KVM/Firecracker), empêchant toute évasion de noyau.

---

### 2. ELEVATION DU PIPELINE MONITORING & LOGGING (EDR & MERKLE LEDGER)
- **Agent Sidecar Falco (eBPF-driven)** :
  - Déployer **Falco** dans le sidecar de chaque cellule pour surveiller les appels système (syscalls) en temps réel.
  - Déclencher immédiatement l'isolation si Falco détecte un spawn d'obusier (reverse shell), une modification de binaire en mémoire, ou une tentative de ptrace.
- **Registre de Logs Immuable (Merkle Tree / RFC 3161)** :
  - Chaîner les logs enregistrés dans `db-log` via un Arbre de Merkle (Merkle Ledger) avec horodatage RFC 3161 garanti, interdisant toute modification ou effacement ultérieur par un attaquant.

---

### 3. HONEYPOT INTERACTIF DYNAMIQUE ET ATTESTATION MATERIELLE
- **Génération Dynamique de Data Leurre via LLM & Canary Tokens** :
  - Utiliser le LLM hors-ligne du Bateau MODELE pour générer dynamiquement des documents piégés (faux bilans, fausses clés API, canary tokens) dans la cellule de `mike-faux`.
  - Configurer un écouteur de canary tokens : si `mike-faux` tente d'utiliser une clé API ou d'ouvrir un canal piégé, l'alerte maximale est déclenchée avec élévation du niveau d'isolation.
- **Attestation Matérielle mTLS / TPM 2.0** :
  - Exiger une preuve d'attestation TPM 2.0 / Enclave Sécurisée lors de l'authentification SSH de `mike-vrai` pour éliminer le risque de vol de clé RSA simple.

---

### 4. OPTIMISATION DU MOTEUR LLM ET STANDARDISATION STIX 2.1
- **Inférence LLM Optimisée (vLLM / GGUF Quantifié)** :
  - Utiliser vLLM ou llama.cpp quantifié (4-bit/8-bit GGUF) sur le Bateau MODELE pour maximiser le débit d'inférence (>30 tokens/sec) tout en maintenant l'empreinte mémoire VRAM sous 8 Go.
  - Conserver le montage `--read-only` strict et `tmpfs` pour zéro persistance malveillante.
- **Standardisation STIX 2.1 / TAXII** :
  - Structurer l'ensemble des Cybercards (attaque, actifs, sécurité, recommandations) selon le schéma **STIX 2.1**, permettant l'export et la synchronisation automatique avec OpenCTI, MISP et les SIEM d'entreprise.
- **Pipeline de Validation Formelle des Vaccins (AST & Non-Régression)** :
  - Avant de soumettre un vaccin au Bateau TEST, exécuter une analyse statique automatisée (Bandit, Shellcheck, AST Python) et vérifier l'absence d'impact négatif sur les performances (RAM/CPU/Bande passante).

---

### 5. INFRASTRUCTURE LAB MULTI-ENTREPRISES (ZKP & GITOPS)
- **Confidentialité Zero-Knowledge (ZKP) & Anonymisation** :
  - Anonymiser les cartes de menaces partagées avec le VPS LAB (nettoyage des IPs, identifiants, configurations internes).
  - Employer des preuves à connaissance nulle (ZKP) pour certifier la véracité des attaques sans exposer la charge utile d'entreprise.
- **Gestion GitOps des Politiques de Sécurité** :
  - Stocker la configuration de sécurité des 5 bateaux dans un dépôt Git local immutable.
  - Chaque validation d'un vaccin génère un commit d'état ; un rollback s'effectue par un simple `git revert`.

---

## CONSIGNES D'EXECUTION ET DE DEPLOIEMENT DES AMELIORATIONS

Veuillez appliquer directement ces modifications dans la base de code, les fichiers Docker Compose, les wrappers CLI et les microservices du projet CYBERSOCLE afin d'implémenter ce niveau de sécurité de classe industrielle.
