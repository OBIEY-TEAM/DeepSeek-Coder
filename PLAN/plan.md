# SPÉCIFICATIONS TECHNIQUES ET ARCHITECTURE GLOBALE DU PROJET CYBERSOCLE

---

## 1. PRÉSENTATION GÉNÉRALE ET VISION DU PROJET

**CYBERSOCLE** est une plateforme hybride de cyber-sécurité (mêlant micro-segmentation réseau eBPF, conteneurisation immuable et durcie, passerelle SSH de déception, pot de miel/honeypot dynamique, EDR sidecar, registre de logs immuable Merkle Ledger, intelligence artificielle locale LLM hors-ligne, analyse vectorielle Qdrant, et validation formelle de vaccins de sécurité).

### Concept Fondateur des 5 Bateaux
Dans l'architecture CYBERSOCLE, une enclave d'infrastructure isolée est désignée par l'analogie d'un **Bateau**.
Chaque environnement CYBERSOCLE (qu'il s'agisse du VPS d'une Entreprise Cliente ou du VPS LAB Central dirigé par OBIEY Christ Dany) est strictement découpé en **5 Bateaux principaux** :
1. **Bateau OFFICIEL** : Zone de production pour les conteneurs/cellules des utilisateurs légitimes (`mike-vrai`).
2. **Bateau PRISON** : Zone de quarantaine sandbox / pot de miel (honeypot) pour isoler les attaquants, fichiers malveillants et sessions de comptes suspects (`mike-faux`).
3. **Bateau MODELE** : Container maître hybride hébergeant le LLM principal en mode hors-ligne (`offline-first`). Il dispose d'un accès en **lecture seule strict** (`--read-only`, `tmpfs`) sur les volumes de bases de données.
4. **Bateau SCIENCE (Threat-Intel-Lab)** : Container hébergeant la base vectorielle Qdrant et le moteur d'apprentissage Python. Relié **uniquement** au Bateau MODELE via un réseau privé restreint (`internal: true`).
5. **Bateau TEST** : Zone d'expérimentation isolée permettant de tester la viabilité, la syntaxe (AST), la sécurité (Bandit) et l'impact de performance des vaccins de sécurité générés.

---

## 2. ARCHITECTURE DÉTAILLÉE DES BATEAUX, VLAN ET RÉSEAU PRIVÉ

### Spécification des Réseaux Docker & Micro-segmentation eBPF
- **Nom du Réseau Virtuel Privé** : `reseau-prive`
- **Configuration Docker Compose** :
  - `driver: bridge`
  - `internal: true` (Bloque tout accès internet direct sortant/entrant pour MODELE, SCIENCE et TEST).
  - Inter-Container Communication (ICC) désactivé par défaut (`com.docker.network.bridge.enable_icc: false`).
- **Plage IP Statique Dédiée** :
  - Passerelle réseau : `172.28.0.1`
  - Bateau OFFICIEL : `172.28.0.10`
  - Bateau PRISON : `172.28.0.20`
  - Bateau MODELE : `172.28.0.30`
  - Bateau SCIENCE : `172.28.0.40`
  - Bateau TEST : `172.28.0.50`
- **Micro-segmentation eBPF Cilium CNI** :
  - Application de règles de filtrage au niveau du noyau Linux (L3/L4/L7).
  - Le Bateau SCIENCE ne peut communiquer **qu'avec le Bateau MODELE**. Tout autre trafic est rejeté au niveau eBPF.
  - Le Bateau MODELE peut lire les données d'OFFICIEL, PRISON et communiquer avec SCIENCE via API interne exclusive.

---

## 3. SPÉCIFICATIONS DES CELLULES (CONTENEURS IMMUABLES, CGROUPS & FIRECRACKER)

### Anatomie d'une Cellule
Une **Cellule** désigne un conteneur Linux géré par le démon Docker Engine / `containerd`.

### Directives de Durcissement et d'Isolation
1. **Namespaces & Cgroups v2** : Isolation stricte des vues processus/réseau et limite mémoire maximale imposée à 2 Go RAM par cellule.
2. **Mode Rootless Docker** : Le démon Docker et les conteneurs tournent en mode non-privilégié sans droits root sur l'hôte VPS.
3. **Profils Seccomp & AppArmor / SELinux** :
   - Blocage des appels système critiques (`ptrace`, `sys_admin`, `kexec_load`, `unshare`, `module_load`).
4. **Système de Fichiers Immuable** :
   - Montage du système de fichiers racine en lecture seule (`docker run --read-only`).
   - Utilisation de volumes temporaires `tmpfs` non-persistants pour les opérations temporaires requises.
5. **Micro-cellules Coffre-fort (MicroVMs Firecracker / Kata Containers)** :
   - Pour le Bateau PRISON et les cellules isolées d'utilisateurs suspects, l'exécution s'effectue au sein d'une micro-VM Firecracker / KVM ultra-légère (démarrage < 100 ms) offrant une étanchéité matérielle contre les évasions de noyau (kernel breakout).

---

## 4. AUTHENTIFICATION SÉCURISÉE, MIKE-VRAI VS MIKE-FAUX ET DÉCEPTION HONEYPOT

### Gateway Proxy SSH Dynamique
- **Mécanisme d'Authentification Multi-Niveaux** :
  1. **Identifiants classiques** : Nom d'utilisateur et mot de passe (ex: `mike` / `mike_secure_pass_2025`).
  2. **Clé de chiffrement locale** : Vérification de la présence d'une clé RSA/Ed25519 spécifique issue du vrai poste de travail.
  3. **Attestation Matérielle TPM 2.0 / mTLS** : Vérification de la signature cryptographique TPM et de la citation PCR.
  4. **Agent IA d'Analyse Comportementale** : Évaluation de la vitesse de frappe, de la vélocité des commandes, des heures de connexion et des appels système.

### Routage Dynamique de Déception
- **Cas `mike-vrai`** :
  - Conditions : Mot de passe valide + Clé locale valide + Attestation TPM conforme + Score d'anomalie comportementale < 0.60.
  - Action : Redirection vers sa cellule de travail saine dans le Bateau OFFICIEL avec accès aux ressources distantes de l'entreprise via tunnel VPN.
- **Cas `mike-faux`** :
  - Conditions : Identifiants valides mais absence de clé locale OU attestation TPM invalide OU comportement suspect (score IA >= 0.60).
  - Action : Redirection transparente vers une cellule clone isolée dans le Bateau PRISON avec fausses données (honeypot). Tous les `mike-faux` accèdent à cette même cellule leurre. Le VPN entreprise leur est strictement refusé.
- **Honeypot Dynamique LLM & Canary Tokens** :
  - Faux documents d'entreprise (PDF, Excel) générés dynamiquement par le LLM.
  - Insertion de Canary Tokens (clés API/AWS fictives piégées). Toute tentative d'utilisation d'une clé canary déclenche l'alerte d'isolation maximale.

---

## 5. LOGGING UNIDIRECTIONNEL, SIDECAR FALCO ET MERKLE LEDGER

### Architecture Sidecar
- **Sidecar Espion Falco (eBPF)** :
  - Chaque cellule est accompagnée d'un conteneur sidecar léger (~20 Mo RAM).
  - Il observe en temps réel les appels système (`syscalls`) depuis l'extérieur du conteneur sans s'y introduire.
- **Tuyau Unidirectionnel (Valve)** :
  - Les logs sont expédiés via Rsyslog / Fluent-Bit vers la base de données dédiée (`db-log`). Le conteneur utilisateur ne possède aucun accès direct à la BDD de logs.
- **Registre de Logs Immuable (Merkle Ledger / RFC 3161)** :
  - Chaque entrée de log est intégrée dans un Arbre de Merkle (Merkle Tree).
  - Horodatage qualifié RFC 3161 certifiant l'immuabilité et l'infalsificabilité des preuves cryptographiques.

---

## 6. MOTEUR LLM EN LECTURE SEULE ET CYBERCARTOGRAPHIE STIX 2.1

### Bateau MODELE (LLM Master)
- **Moteur d'Inférence Optimisé** :
  - Utilisation de **vLLM / llama.cpp (quantification GGUF 4-bit / 8-bit)** pour garantir un débit > 30 tokens/sec tout en maintenant l'empreinte VRAM sous 8 GB.
  - Fonctionne en mode 100% hors-ligne (offline-first).
  - Montage de tous les volumes de bases de données (`db-prod-cluster`, `db-quarantaine-sandbox`, `db-log`, `db-agent-ai`) en **lecture seule strict** (`--read-only`, `tmpfs`).

### Standardisation STIX 2.1 & 4 Cybercards
Toute Cybercartographie générée par le Bateau MODELE est un document JSON conforme à la norme internationale **STIX 2.1**, découpé en 4 Cybercards modulaires :
1. `cybercard_attaque` : Type d'attaque, vecteur d'entrée, signature contextuelle (Indicator).
2. `cybercard_actifs` : Fichiers ciblés, processus affectés, ressources d'entreprise (Infrastructure).
3. `cybercard_securite` : Mesures de sécurité actives au moment de l'impact (Course-of-action).
4. `cybercard_recommandation` : Actions correctives et règles du vaccin de sécurité proposé (Course-of-action).

### Signature Cryptographique SHA256
- Chaque bundle de Cybercartographie est signé avec un hash SHA256 par le Bateau MODELE (`signed_by: BATEAU_MODELE_LLM_MASTER`).
- Le Bateau SCIENCE vérifie la signature à la réception et rejette automatiquement tout document non conforme.

---

## 7. GESTION DES INCIDENTS, CLONAGE ET RÈGLES DE RÉGÉNÉRATION

### Processus d'Isolation d'une Cellule
1. **Détection** : Alerte levée par le sidecar Falco ou l'agent IA.
2. **Micro-segmentation** : Rupture immédiate du lien réseau de la cellule compromise via règle eBPF Cilium.
3. **Cybercartographie Pré-isolation** : Génération immédiate d'un rapport STIX 2.1 avant neutralisation.
4. **Clonage & Redirection** : La cellule est clonée vers le Bateau PRISON, la session utilisateur est transparente basculée vers ce clone, et la cellule d'origine dans OFFICIEL est détruite.
5. **Garde-fou Anti-Épuisement de Ressources** : Seuil maximal imposé sur le nombre de clones actifs (`MAX_PRISON_CLONES = 10`) et le rythme de clonage (`MAX_CLONE_RATE_PER_MIN = 5`) pour empêcher le déni de service de l'hôte VPS.

### Règles de Régénération des Bateaux
- **Régénération du Bateau OFFICIEL** :
  - Déclenchée en cas d'infection majeure de l'enclave OFFICIEL.
  - Génération d'un deuxième Bateau OFFICIEL sain. SSH temporairement bloqué, alerte client transmise.
  - Double authentification (2FA) obligatoire sur les 10 accès suivants, avec validation explicite par l'entreprise lors du premier accès.
- **Régénération du Bateau PRISON** :
  - Déclenchée en cas d'évasion d'un virus ou de `mike-faux` vers l'enclave PRISON.
  - Génération d'un deuxième Bateau PRISON sain, transfert des cellules non compromises, envoi de la Cybercartographie STIX 2.1 au Bateau SCIENCE, puis destruction de l'ancien Bateau PRISON.
- **Réinitialisation du Bateau SCIENCE** :
  - Restauration possible à partir du dernier checkpoint sain enregistré (`v1.0.0`).

---

## 8. BATEAU SCIENCE (THREAT-INTEL-LAB) ET BATEAU TEST (VALIDATION FORMELLE)

### Bateau SCIENCE (Threat-Intel-Lab)
- Héberge la base vectorielle **Qdrant** et le moteur d'apprentissage Python.
- Traite les Cybercartographies STIX 2.1 pour faire ressortir les modèles de vulnérabilités, évaluer les risques et construire des scripts/programmes de renforcement ("vaccins").

### Bateau TEST & Pipeline de Validation Formelle
Chaque vaccin généré fait l'objet d'un pipeline de qualification rigoureux sur le Bateau TEST :
1. **Analyse Statique de Syntax (AST Python)** : Validation du parsing AST pour éliminer tout bug de syntaxe.
2. **Analyse de Sécurité Code (Bandit Scanner)** : Interdiction d'instructions dangereuses (`eval`, `exec`, `os.system`).
3. **Mesure d'Impact de Performance** : Vérification que la surconsommation CPU reste < 2.0% et RAM < 10 Mo.
4. **Score de Confiance (0.0 à 1.0)** :
   - Un vaccin avec score >= 0.90 et criticité moyenne/faible est auto-approuvé (`APPROVED_AUTOMATICALLY`).
   - Les vaccins à criticité `HIGH` ou `CRITICAL` requièrent obligatoirement la validation humaine.
5. **Rollback Automatique** : En cas de pic d'anomalie post-déploiement (CPU > 85%, taux d'erreur > 5%), le système applique un rollback immédiat.
6. **Réinitialisation automatique** du Bateau TEST à son état snapshot initial après chaque batterie de tests.

---

## 9. INTERFACE ADMIN WEB REACT / FASTAPI ET GITOPS

### Application Web Admin
- Backend FastAPI (`cybersocle/web/api_backend.py`) et Interface Web React HTML (`cybersocle/web/ui_app.py`) hébergés dans une cellule restreinte `admin-security` accessible via VPN/SSH.
- Permet à l'administrateur sécurité d'examiner les vaccins en attente et de valider leur déploiement en 1 clic.

### Gestion GitOps des Politiques de Sécurité
- Le gestionnaire GitOps (`cybersocle/ecosystem/gitops_manager.py`) maintient l'historique des états de sécurité dans un dépôt Git local (`.cybersocle_gitops`).
- Chaque vaccin appliqué génère un commit d'état. Un rollback vers toute version antérieure (`V1`, `V1.0.1`, `V2`) s'effectue de manière déterministe via `git revert`.

---

## 10. ÉCOSYSTÈME MULTI-ENTREPRISES ET VPS LAB CYBERSOCLE (OBIEY CHRIST DANY)

### Architecture Globale du LAB CYBERSOCLE
- Le VPS LAB CYBERSOCLE (propriété de l'équipe CYBERSOCLE et des co-fondateurs OBIEY Christ Dany) possède sa propre instance 5 Bateaux.
- Connexion VPN sécurisée reliant les bateaux PRISON, SCIENCE et TEST des entreprises clientes aux bateaux PRISON, SCIENCE et TEST du LAB.

### Confidentialité Zero-Knowledge Proofs (ZKP) & Anonymisation
- **Anonymisation stricte** : Avant toute transmission vers le VPS LAB, le module d'anonymisation nettoie la Cybercartographie STIX 2.1 de toute adresse IP, nom d'utilisateur ou chemin interne entreprise.
- **Preuves ZKP (Zero-Knowledge Proofs)** : Certification cryptographique prouvant la réalité de l'attaque subie sans dévoiler le contenu confidentiel de l'entreprise.

### Boucle de Circulation des Vaccins
1. Attaque interceptée sur le Bateau PRISON-Entreprise -> Cybercartographie ZKP transmise au LAB.
2. Génération/amélioration du vaccin dans SCIENCE-LAB.
3. Qualification sur Bateau TEST-LAB et validation humaine par l'équipe LAB (OBIEY Christ Dany).
4. Diffusion aux Bateaux SCIENCE des autres entreprises clientes pour application après validation locale.

---

## 11. COMMANDES DE DÉPLOIEMENT CLI

L'outil CLI `cybersocle/cli.py` permet d'initialiser et de déployer le système selon le rôle de la machine host :

### Déploiement sur VPS Entreprise Cliente :
```bash
python -m cybersocle.cli --client
```
*Initialise les 5 Bateaux clients, configure le réseau `reseau-prive` avec règles eBPF Cilium, active la passerelle SSH de déception et le pont VPN vers le LAB.*

### Déploiement sur VPS LAB CYBERSOCLE (OBIEY Christ Dany) :
```bash
python -m cybersocle.cli --lab
```
*Initialise les 5 Bateaux du LAB Central, configure le concentrateur VPN multi-entreprises, le hub d'anonymisation ZKP et le registre global des vaccins.*
