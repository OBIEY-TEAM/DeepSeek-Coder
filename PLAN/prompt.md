# PROMPT DE GENERATION ET DE CONSTRUCTION DU PROJET CYBERSOCLE

Vous êtes un Architecte Système Cyber-Sécurité, Ingénieur DevOps/Cloud Infrastructure et Développeur Principal Expert. Votre mission est de concevoir, implémenter, conteneuriser et déployer l'intégralité du projet **CYBERSOCLE** à partir des spécifications fonctionnelles et techniques contenues dans `PLAN/plan.md`.

---

## CONTEXTE ET PHIOLOSOPHIE DU PROJET

**CYBERSOCLE** est un projet hybride de cyber-sécurité (combinaison d'agents légers localisés, de conteneurisation isolée, de pot de miel/déception et d'intelligence artificielle locale via LLM).
L'analogie de base repose sur l'image d'un **Bateau** pour désigner une enclave/environnement Docker isolé. Le système global se compose de **5 Bateaux principaux** par infrastructure cliente et par laboratoire central.

---

## INSTRUCTIONS DÉTAILLÉES PAR COMPOSANT & ARCHITECTURE

### 1. TOPO-ARCHITECTURE DES 5 BATEAUX ET VLAN PRIVE
Vous devez orchestrer et déployer 5 bateaux (enclaves Docker / VLANs stricts):
1. **Bateau OFFICIEL** : Héberge les cellules de production assignées aux utilisateurs connectés via SSH.
2. **Bateau PRISON** : Zone de quarantaine sandbox / pot de miel (honeypot) pour isoler les attaquants, fichiers malveillants et sessions de comptes suspects (`mike-faux`).
3. **Bateau MODELE** : Container maître hybride hébergeant le LLM principal en mode hors-ligne (offline-first). Il possède un accès en **lecture seule strict** (`--read-only`, `tmpfs`) sur les volumes de bases de données (prod, sandbox, logs, agents).
4. **Bateau SCIENCE (threat-intel-lab)** : Container hébergeant une base vectorielle Qdrant et un moteur d'apprentissage Python. Relié **uniquement** au Bateau MODELE via une API interne exclusive sur le réseau Docker privé (`internal: true`).
5. **Bateau TEST** : Zone d'expérimentation isolée permettant de tester la viabilité et l'innocuité des patchs, scripts de sécurité et "vaccins" générés.

---

### 2. ARCHITECTURE DES CELLULES (CONTENEURS & MICRO-CELLULES)
- **Définition d'une Cellule** : Un conteneur Linux géré via Docker Engine / démon Docker.
- **Ressources & Isolation** :
  - **Namespaces & Cgroups** : Micro-segmentation stricte (ex: limite mémoire à 2 Go RAM par cellule).
  - **Conteneurs Immuables et Durcis** :
    1. Système de fichiers principal en lecture seule (`docker run --read-only`).
    2. Suppression des ports d'entrée (pas de SSH/Internet entrant sur les cellules durcies agents).
    3. Image Distroless (suppression de `bash`, `apt`, etc.).
  - **Micro-cellule Coffre-fort (Firecracker / Béton)** :
    - Micro-VM/conteneur ultra-durci hébergeant les fausses données générées aléatoirement (PDF, images, dossiers, programmes légers) pour l'isolation d'utilisateurs frauduleux.

---

### 3. LOGIQUE D'AUTHENTIFICATION, DECEPTION & GESTION DE MIKE-VRAI / MIKE-FAUX
- Implémenter un proxy/passerelle d'authentification SSH dynamique à l'entrée du Bateau OFFICIEL :
  - Lors d'une tentative de connexion (ex. utilisateur `mike`) :
    - Vérifier la validité des identifiants ET la présence d'une **clé de chiffrement valide** provenant du vrai poste de travail local.
    - **Si `mike-vrai` (clé valide)** : Redirection vers sa vraie cellule de travail dans le Bateau OFFICIEL avec accès aux ressources distantes de l'entreprise via tunnel VPN VPS.
    - **Si `mike-faux` (clé invalide / pirate)** : Redirection transparente par défaut vers une cellule clone isolée dans le Bateau PRISON contenant de fausses données (honeypot). Tous les faux-mike partagent cette même cellule fausse.
  - Dans la cellule : Mise à disposition d'un navigateur sécurisé orientant le trafic vers les applications d'entreprise via VPN pour les cellules saines uniquement.

---

### 4. PIPELINE DE LOGS RSYSLOG/FLUENT-BIT (ESPION SIDECAR)
- **Sidecar Espion** :
  - Chaque cellule est accompagnée d'un conteneur sidecar ultra-léger (~20 Mo RAM) collé à l'extérieur.
  - Il observe et capture le flux d'exécution et les logs sans jamais s'introduire dans la cellule.
- **Tuyau unidirectionnel (Valve)** :
  - Le conteneur interne ne peut pas communiquer directement avec la base de données logs.
  - Le sidecar transfère les logs via Rsyslog / Fluent-Bit vers la base de données de logs dédiée (`db-log`) de la cellule sur un réseau isolé.

---

### 5. GESTION DES INCIDENTS, ISOLATION ET REGENERATION DYNAMIQUE
- **Détection de menace & Isolation d'une cellule** :
  1. Déclenchement d'une alarme en cas d'envoi de fichier malveillant.
  2. Rupture immédiate du lien réseau (micro-segmentation de quarantaine) sans éteindre la cellule.
  3. Génération d'une **Cybercartographie pré-isolation**.
  4. Clonage de la cellule affectée vers le Bateau PRISON et suppression de la cellule impactée dans OFFICIEL.
  5. Redirection de la session utilisateur compromise vers le clone isolé dans PRISON.
- **Régénération du Bateau OFFICIEL** :
  - En cas d'infection au niveau du Bateau OFFICIEL : Régénération d'un deuxième Bateau OFFICIEL à l'état sain. SSH bloqué et alerte transmise à l'entreprise. Double authentification (2FA) obligatoire sur les 10 accès suivants.
- **Régénération du Bateau PRISON** :
  - En cas d'évasion d'un virus ou de `mike-faux` depuis sa cellule vers le Bateau PRISON : Génération automatique d'un deuxième Bateau PRISON sain, clonage de toutes les cellules isolées sauf celle de l'attaquant, envoi de sa Cybercartographie au Bateau SCIENCE, puis destruction de l'ancien Bateau PRISON.

---

### 6. CYBERCARTOGRAPHIE & FORMAT DES CYBERCARDS (JSON)
Chaque rapport de Cybercartographie généré par le Bateau MODELE est un document JSON structuré en 4 Cybercards modulaires :
1. `cybercard_attaque` : Type d'attaque, vecteur d'entrée, signature contextuelle.
2. `cybercard_actifs` : Fichiers touchés, processus, ressources ciblées.
3. `cybercard_securite` : Mesures de sécurité appliquées au moment de l'impact.
4. `cybercard_recommandation` : Actions correctives et règles de renforcement proposées.
- **Signature Cryptographique** : Chaque Cybercard est signée avec un hash SHA256 par le Bateau MODELE. Le Bateau SCIENCE vérifie obligatoirement la signature à la réception et rejette tout document invalide.

---

### 7. BATEAU SCIENCE (THREAT-INTEL-LAB), BATEAU TEST ET AXIOME DES VACCINS
- **Threat-Intel-Lab (Container 4 Science)** :
  - Reçoit les Cybercartographies validées.
  - Utilise la base vectorielle Qdrant et le moteur Python pour entraîner des modèles localisés, évaluer menaces/vulnérabilités et construire des scripts/programmes de renforcement ("vaccins").
- **Validation sur Bateau TEST & Interface Web React / API** :
  - Les correctifs sont automatiquement exécutés sur le Bateau TEST.
  - Si le test est positif : Une alerte remonte sur l'application Web React (API backend sécurisée via VPN/SSH sur une cellule `admin-security`).
  - L'administrateur sécurité valide manuellement le déploiement par un clic.
- **Ecosystème Multi-Entreprises & VPS LAB (OBIEY Christ Dany)** :
  - Connexion VPN entre les bateaux PRISON/SCIENCE/TEST des entreprises et le VPS LAB CYBERSOCLE.
  - Les vaccins testés positifs dans une entreprise sont transmis au LAB, re-testés, validés par l'équipe LAB, puis proposés aux autres entreprises clientes.
  - Prise en charge du versionnage des vaccins (V1, V1.0.1, V2...) avec possibilité de rollback vers les versions antérieures.

---

## CONSIGNES DE DÉPLOIEMENT & DE DÉVELOPPEMENT

1. **Docker Compose & Scripts Bash/Python** : Créez la configuration `docker-compose.yml` avec l'ensemble des 5 services/bateaux, réseaux `internal: true`, volumes read-only et limites Cgroups.
2. **Scripts d'automatisation & CLI** : Fournir une commande de déploiement pour VPS entreprise client (`cybersocle-deploy --client`) et une commande pour le VPS LAB (`cybersocle-deploy --lab`).
3. **Robustesse & Offline-First** : Garantir l'absence totale de dépendance Internet pour les bateaux MODELE, SCIENCE et TEST.

Veuillez générer le code source, les fichiers de configuration, les conteneurs Docker et les API nécessaires à l'exécution intégrale de ce système CYBERSOCLE.
