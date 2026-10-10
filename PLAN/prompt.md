# PROMPT GLOBAL DE GÉNÉRATION, ARCHITECTURE ET DÉPLOIEMENT DU PROJET CYBERSOCLE

Vous êtes un Architecte Système Cyber-Sécurité, Ingénieur DevOps/Cloud Infrastructure et Développeur Principal Expert. Votre mission est de concevoir, implémenter, conteneuriser et déployer l'intégralité de la plateforme **CYBERSOCLE** à partir des spécifications fonctionnelles et techniques révisées contenues dans `PLAN/plan.md` et `PLAN/amelioration.md`.

---

## 1. CONTEXTE ET PHILOSOPHIE DU PROJET

**CYBERSOCLE** est un système hybride de cyber-sécurité combinant micro-segmentation réseau eBPF, conteneurisation immuable et durcie, passerelle de déception SSH avec honeypot dynamique, agents espions sidecars eBPF/Falco, registre de logs immuable basé sur les Arbres de Merkle, cartographie de menaces hors-ligne augmentée par LLM local (STIX 2.1 Cybercards), moteur d'apprentissage vectoriel (Qdrant Threat-Intel-Lab), et infrastructure multi-entreprises reliée au VPS LAB CYBERSOCLE (co-fondateur OBIEY Christ Dany).

L'analogie de base repose sur l'image d'un **Bateau** pour désigner un domaine d'isolation / enclave Docker d'infrastructure. Le système se compose de **5 Bateaux principaux** déployés de manière identique sur le VPS de chaque Entreprise Cliente et sur le VPS LAB Central.

---

## 2. TOPO-ARCHITECTURE DES 5 BATEAUX ET RÉSEAU PRIVÉ (VLAN / eBPF)

Vous devez orchestrer et déployer 5 bateaux (enclaves Docker sur le réseau virtuel privé `reseau-prive` avec `internal: true` et filtrage eBPF Cilium CNI) :

1. **Bateau OFFICIEL** :
   - Héberge les cellules de production assignées aux utilisateurs légitimes connectés via SSH.
   - Relié aux ressources réseau distantes de l'entreprise via tunnel VPN VPS uniquement pour les utilisateurs authentifiés (`mike-vrai`).

2. **Bateau PRISON** :
   - Zone de quarantaine sandbox / honeypot dynamique pour isoler les attaquants, fichiers malveillants et sessions de comptes suspects (`mike-faux`).
   - Contient des leurres actifs, canary tokens et fausses données dynamiquement générées par IA.

3. **Bateau MODELE** :
   - Container maître hybride hébergeant le LLM principal en mode hors-ligne (offline-first) via **vLLM / llama.cpp (GGUF quantifié 4/8-bit)**.
   - Possède un accès en **lecture seule strict** (`--read-only`, `tmpfs`) sur les volumes de bases de données (prod, sandbox, logs, agents).
   - Accès réseau restreint sans aucune sortie internet.

4. **Bateau SCIENCE (Threat-Intel-Lab)** :
   - Container hébergeant la base vectorielle **Qdrant** et le moteur d'apprentissage Python.
   - Relié **uniquement** au Bateau MODELE via une API interne exclusive (`internal: true`) sur le réseau privé Docker.
   - Génère les modèles de risques, évalue les vulnérabilités et construit des scripts/programmes de renforcement ("vaccins").

5. **Bateau TEST** :
   - Zone d'expérimentation ultra-isolée permettant de tester la viabilité, l'innocuité et les performances (AST Python, Bandit, tests de charge CPU/RAM) des vaccins de sécurité.
   - Réinitialisation automatique à l'état sain (snapshot) après chaque session de validation.

---

## 3. SPÉCIFICATIONS DES CELLULES (DURCISSEMENT & ISOLATION)

- **Définition d'une Cellule** : Un conteneur Linux géré via Docker Engine / containerd.
- **Micro-segmentation & Isolation** :
  - Namespaces, Cgroups v2 (limite stricte à 2 Go RAM par cellule).
  - Mode Rootless Docker pour éliminer les privilèges `root` sur l'hôte.
  - Profils **Seccomp** (interdisant `ptrace`, `kexec_load`, `sys_admin`, `unshare`) et profils **AppArmor / SELinux** durcis.
  - Système de fichiers principal immuable (`--read-only` avec `tmpfs` temporaire).
  - Suppression de tout port d'entrée direct (pas de SSH/Internet entrant sur les cellules agents durcies).
  - Micro-VMs **Firecracker / Kata Containers** pour les cellules du Bateau PRISON et les environnements à haut risque.

---

## 4. AUTHENTIFICATION SÉCURISÉE, DÉCEPTION SSH & HONEYPOT DYNAMIQUE

- **Passerelle Proxy SSH Dynamique** à l'entrée du Bateau OFFICIEL :
  - **Vérification Multi-Facteurs & Matérielle** : Valide le mot de passe, la présence de la clé de chiffrement locale, et l'attestation matérielle **TPM 2.0 / mTLS** du poste de travail.
  - **Agent IA d'Analyse Comportementale** : Analyse la dynamique de session (cadence de frappe, vélocité des commandes, appels système inhabituels, heures de connexion).
  - **Axiome Mike-Vrai vs Mike-Faux** :
    - Si `mike-vrai` (clé valide + attestation TPM + comportement normal) -> Accès à sa cellule de travail saine dans OFFICIEL avec tunnel VPN entreprise.
    - Si `mike-faux` (clé invalide / pas de TPM / comportement anormal détecté par l'agent IA) -> Redirection transparente par défaut vers une cellule clone isolée dans Bateau PRISON avec fausses données et canary tokens. Tous les `mike-faux` partagent cette cellule leurre.
  - **Honeypot Dynamique LLM & Canary Tokens** :
    - Le LLM du Bateau MODELE alimente la cellule fausse avec de faux documents dynamiques crédibles et des canary tokens (clés API/AWS piégées).
    - Toute tentative d'utilisation d'un canary token déclenche immédiatement une alerte maximale et renforce l'isolement.

---

## 5. PIPELINE DE LOGGING UNIDIRECTIONNEL & EDR SIDECAR (FALCO + MERKLE LEDGER)

- **Sidecar Espion Falco (eBPF)** :
  - Chaque cellule est couplée à un conteneur sidecar léger (~20 Mo RAM) exploitant **Falco eBPF** pour surveiller les appels système (`syscalls`) à l'extérieur de la cellule.
  - Détecte immédiatement les comportements suspects (reverse-shells, injections mémoire, modifications de binaires).
- **Tuyau Unidirectionnel (Valve)** :
  - Transfert unidirectionnel des logs via Rsyslog / Fluent-Bit vers la base de données dédiée (`db-log`).
- **Registre de Logs Immuable (Merkle Tree / RFC 3161)** :
  - Les logs sont scellés cryptographiquement au fil de l'eau dans un Arbre de Merkle (Merkle Ledger) avec horodatage RFC 3161 certifié, garantissant l'immuabilité totale des preuves.

---

## 6. CYBERCARTOGRAPHIE STIX 2.1 & FORMAT DES CYBERCARDS

- **Moteur LLM Master hors-ligne (Bateau MODELE)** :
  - Inférence optimisée vLLM / GGUF (< 8 GB VRAM, > 30 tokens/sec).
  - Inspecte les logs en lecture seule (`--read-only`) et génère les Cybercartographies structurées selon la norme internationale **STIX 2.1**.
- **4 Cybercards Modulaires** :
  1. `cybercard_attaque` (Indicator / Attack pattern) : Type d'attaque, vecteur d'entrée, signature contextuelle.
  2. `cybercard_actifs` (Infrastructure / Assets) : Fichiers ciblés, processus affectés, ressources d'entreprise.
  3. `cybercard_securite` (Course of Action / Security) : Mesures actives au moment de l'impact.
  4. `cybercard_recommandation` (Course of Action / Recommendations) : Actions correctives et règles du vaccin de sécurité proposé.
- **Signature Cryptographique SHA256** :
  - Le Bateau MODELE signe cryptographiquement le bundle JSON STIX 2.1.
  - Le Bateau SCIENCE vérifie obligatoirement la signature SHA256 à la réception et rejette tout document invalide.

---

## 7. ISOLATION DES INCIDENTS, CLONAGE & RÈGLES DE RÉGÉNÉRATION

- **Détection & Isolation Réseau** :
  - En cas d'attaque détectée dans une cellule OFFICIEL, la micro-segmentation eBPF coupe immédiatement tous les accès réseau de la cellule (sauf le tuyau sidecar).
  - La cellule est clonée vers le Bateau PRISON, la session utilisateur compromise est redirigée vers le clone, et la cellule d'origine dans OFFICIEL est détruite.
- **Garde-fou Anti-Épuisement de Ressources** :
  - Limite stricte sur le rythme de clonage et le nombre maximum de cellules/bateaux PRISON actifs pour prévenir les attaques par déni de service (DoS/RAM exhaustion).
- **Régénération du Bateau OFFICIEL** :
  - En cas d'infection majeure de la structure OFFICIEL : Régénération d'un Bateau OFFICIEL à l'état sain. SSH bloqué, alerte entreprise transmise. Double authentification (2FA) obligatoire sur les 10 accès suivants, et validation client requise lors de la première reconnexion.
- **Régénération du Bateau PRISON** :
  - En cas d'évasion d'un virus ou de `mike-faux` depuis sa cellule vers le Bateau PRISON : Génération d'un deuxième Bateau PRISON sain, clonage des cellules isolées non compromises, transmission de la Cybercartographie STIX 2.1 au Bateau SCIENCE, puis destruction de l'ancien Bateau PRISON.
- **Restauration du Bateau SCIENCE** :
  - Possibilité de réinitialisation à partir du dernier checkpoint sain versionné (`v1.0.0`).

---

## 8. BATEAU SCIENCE (THREAT-INTEL-LAB), BATEAU TEST & VACCINATION FORMELLE

- **Threat-Intel-Lab (Bateau SCIENCE)** :
  - Reçoit les cartographies STIX 2.1 signées, stocke les embeddings dans la base vectorielle Qdrant, et entraîne des modèles locaux pour classifier menaces et générer des vaccins (code/scripts de durcissement).
- **Validation Formelle sur Bateau TEST** :
  - Analyse statique de code obligatoire (AST Python, Bandit security scanner) et mesure de l'impact de performance (CPU, RAM, bande passante).
  - Calcul d'un **Score de Confiance (0.0 à 1.0)** : Auto-approbation si score >= 0.90 (sauf si criticité CRITICAL/HIGH qui requiert toujours la validation humaine).
  - En cas d'anomalie post-déploiement, déclenchement d'un rollback automatique.
  - Réinitialisation automatique du Bateau TEST après chaque batterie de tests.

---

## 9. INTERFACE ADMIN WEB REACT / FASTAPI & GITOPS

- **Interface Admin de Validation Humaine** :
  - Application Web React / API Backend FastAPI tournant dans une cellule sécurisée `admin-security` accessible via VPN/SSH.
  - Permet aux administrateurs sécurité de visualiser les recommandations classées par score de confiance et d'approuver en 1 clic le déploiement d'un vaccin.
- **Gestion GitOps des Politiques de Sécurité** :
  - Chaque vaccin déployé génère un commit d'état signé dans le dépôt GitOps local (`.cybersocle_gitops`).
  - Possibilité de rollback instantané vers toute version antérieure (V1, V1.0.1, V2) par simple `git revert`.

---

## 10. ÉCOSYSTÈME MULTI-ENTREPRISES & LAB CYBERSOCLE (OBIEY Christ Dany)

- **Architecture Cloud Hybride** :
  - Chaque Entreprise Cliente possède son instance 5 Bateaux (OFFICIEL, PRISON, MODELE, SCIENCE, TEST).
  - Le VPS LAB CYBERSOCLE (dirigé par OBIEY Christ Dany) possède sa propre instance 5 Bateaux centrale.
  - Tunnels VPN sécurisés interconnectant les bateaux PRISON, SCIENCE et TEST clients avec ceux du LAB.
- **Confidentialité Zero-Knowledge Proofs (ZKP) & Anonymisation** :
  - Anonymisation automatique complète des Cybercartographies transmises au LAB (nettoyage des adresses IP, identifiants, chemins internes).
  - Utilisation de preuves ZKP pour prouver l'existence réelle d'une attaque sans exposer les données sensibles de l'entreprise.
- **Boucle de Distribution de Vaccins** :
  - Les vaccins testés positifs dans une entreprise sont anonymisés et transmis au LAB, re-testés dans TEST-LAB, validés par l'équipe LAB (OBIEY Christ Dany), puis distribués aux autres entreprises avec option d'approbation humaine locale.

---

## 11. INSTRUCTIONS ET COMMANDES DE DÉPLOIEMENT CLI

Proposer un outil CLI Python `cybersocle.cli` prenant en charge deux modes d'exécution :

1. **Mode VPS Entreprise Cliente** :
   ```bash
   python -m cybersocle.cli --client
   ```
   Deploy la pile 5 Bateaux client, initialise le réseau `reseau-prive` eBPF Cilium, active le sidecar Falco, la passerelle SSH deception et la connexion VPN au LAB.

2. **Mode VPS LAB CYBERSOCLE (OBIEY Christ Dany)** :
   ```bash
   python -m cybersocle.cli --lab
   ```
   Deploy la pile 5 Bateaux LAB central, initialise le pont VPN multi-entreprises, le hub ZKP et le registre central de distribution de vaccins.

---

Veuillez générer et maintenir le code source, les fichiers de configuration Docker, les profils de sécurité eBPF/Seccomp, les pipelines d'apprentissage et les API nécessaires à l'exécution intégrale du système CYBERSOCLE.
