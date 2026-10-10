# NOM DU PROJET ET PRESENTATION GENERALE

LE NOM DU PROJET C' EST CYBERSOCLE
CE PROJET EST POUR LE MOMENT LLM, JE VEUX QUE CA SOIT UN PROJET HYBRIDE.
Considere un docker comme un bateau.
Le nombre des bâteau est cinq 5 OFFICIEL + PRISON + MODELE + SCIENCE + TEST.
Au redemarrage du VPS n'efface aucune donnée des bateaux,

# ARCHITECTURE DES BATEAUX, VLAN ET RESEAU PRIVE

Une cellule, un container.
L'usine qui fait les bîtes, Docker Engin/ le demon Docker.
C'est la machine qui fabrique les cellules.
Le bateau où les cellules sont réliés, le réseau virtuel (docker network), c'est le fil invisible qui relie les cellules.
Couper le lien entre deux cellule, micro segmentation quarantaire.
Creer des vlan pour mettre des mur entre les différents bateau.
Communication inter vlan pas d'internet via vlan.
Les bateaux MODELE + SCIENCE + TEST doivent etre offline pas d'internet juste des liens offlines entre le bateau MODELE avec le bateau OFFICIEL et le bateau PRISON, lien entre bateau MODELE et bateau SCIENCE pas de liens supplementaires entre bateaux.
Creer 1 réseau qui s'appelle reseau-prive et lui dire internal:true pour la connexion entre les bateaux.
Dans le projet applique la regle du moindre privillège.

# SPECIFICATIONS DES CELLULES (CONTENEURS IMMUABLES, CGROUPS & FIRECRACKER)

La cellule, une petite boîte linux.
L'utilisateur croit qu'il a un vrai pc, mais c'est une boîte légère.
Il a son propre nim, propre mot de passe ssh, propre dossier.
L'utilisateur dedans peut tout casser, le serveur ne risque rien.
Isolation, 2 technologies qui s'appellent Namespaces + Cgroups.
Namespaces dit tu ne vois que ta boîte.
Cgroups dit tu ne peux utiliser que 2Go de ram pas plus.
La boîte très solide en béton, une micro cellule (firecracker), pareil qu'une cellule mais 100% coffre fort.
Plus lours, même un virus tres fort ne peut pas sortir le clone fausse de la cellule vrai.
La cellule clone fausse du vrai a une base de données generer aleatoires avec fosses données fausse pdf et images, dossiers et programmes très legère moins de RAM.
La cellule coffre-fort avec base de donnée ai et agent ia est codé en dur.
Le vrai nom c'est conteneur immuable et durci.
Pourque aucun virus ne puisse y rentrer, fais 3 choses 1= Système en lecture seule: docker run--read--only 2=Pas deporte d'entrée: on coupe le ssh on coupe internet entrant il n'accepte que le tuyau de logs qui arrive on le met sur un reseau isolé 3=Distroles: on enlève tout pas de bash pas de apt juste la base de donnée ia avec petit agent ia.

# AUTHENTIFICATION UTILISATEUR, MIKE-VRAI ET MIKE-FAUX (DECEPTION ET HONEYPOT)

Le client se connecte au bateau officiel via une connexion ssh precisement à une cellule (conteneur) qui lui est attribuer.
Ajoute une logique également pour la connexion d'un utilisateur par exemple mike-vrai et mike-faux pour se connecter autorise les identifiants corrects de se connecter si mike se connecte verifie s'il a une cle de chiffrement valide qui lui est fourni sur son vrai poste de travail en local le mike-vrai en a mais le mike-faux n'a pas autorise le mike-faux a se connecter à une cellule clone avec des fausse données de mike dans le bateau prison par default et le vrai mike a continuer sans travail tous les faux-mike auront acces à la meme fausse à chaque connexion et reconnexion cellule de mike seul le vrai mike aura access a la vrai cellule mike.
Sur le bateau prison le mike-faux est notre hacker du systeme la cellule agent ia genere la cybercartographie apres attache et la cellule log& espion surveille toutes actions durant l'isolation.
Dans ces cellules où se connecte les client vrai et faux met des navigateurs.
Les clients utilisent ses navigateurs par default un emploiyé se connecte à l'application de son entreprise la connexion est dirigee via ssh vers la cellule sur le navigateur via se navigateur il a access au ressources de sont entreprise via VPN une connexion VPS entre cette cellule saine et les ressources distants locaux de l'entreprise mais la cellule affectée n'a pas ce accèss VPN a seulement access ssh entre utilisateur et la cellule.

# LOGGING, SIDECAR ET SURVEILLANCE DES ATTAQUES

Chaque petit agent a aussi sa base de données, donc il y a la base de données des logs et la base de données des petits agents.
Les logs des actions de chaque cellule du systeme dois etre mise dans une base de donnee log dedié pour cette cellule.
Chaque cellule OFFICIEL est connecter à une cellule de lecture, une cellule de log & espion et à une cellule petit agent ia qui est uniquement assistant et regarde les faits et redige les cybercartographies et enregistre dans leurs propre base de donnee db-agent-ai respectives.
Met un petit espion collé à l'exterieur de la boîte que mike-vrai et celle que mike-faux utilisent qui lit ce qui se passe à l'intérieur.
En docker ça s'appelle un sidecar.
Il lit les logs sans jamais rentrer dedans: cet espion est tout^petit, il prend 20 Mo de Ram.
Tu tuyau qui envoie les logs, doit être à sens unique, comme une valve.
La boîte ne peut pas parler à la base de données logs.
C'est l'espion dehors qui passe les logs vers la base de données logs.
On fait ca avec rsyslog ou fluent-bit.
Le virus dans la boîte ne voit même pas le tuyau.
Vérification constant des programmes malveillants sur les cinq bateaux par default et creer des logs des bases de donnees logs pour chaque bateau également et creation d'une cybercartographie en cas d'attaque d'un bateau.

# PETITS AGENTS ET BATEAU MODELE (LLM EN LECTURE SEULE)

Des petit agents ia connecter au LLM via lien sans internet(offline fist) deployés sur le bateau officiel et sur le bateau prison.
Les petits agents qui sont dans les bateaux OFFICIEL et PRISON ne sont pas des ia ce sont juste des petits programmes tout leger qui posent des questions au gros bateau MODELE.
Les petits agents ne parlent pas entre eux.
Un bateau modele avec access à toutes les bases de données du bateau officiel et du bateau prison.
Le MODELE a access aux bases de données des logs et des petits agent ia des bateaux OFFICIEL et PRISON.
Le bateau MODELE contient est le seul container qui contient le LLM montage de tous les volumes de bases de donées en lectures seule -only: volume OFFICIEL db prod-cluster, volume PRISON db quarantaire-sandbox, volume logs DB, volume agents DB.
Lancement en mode filesystem read-only tmpfs pour empêcher toute modification par un virus.

# ISOLATION DES INCIDENTS, CLONAGE DE CELLULE ET REGENERATION DU BATEAU PRISON ET OFFICIEL

La cellule isolé reste allumée,elle fonctionne.
Quand un virus ou un fichier programme ou autre truc malveillant est envoyé dans une cellule du bateau malveillant où l'utilisateur est connecté via ssh une alarme est déclenché puis cette cellule des déliée des autres puis la copie de cette cellule est creer dans le bateau prison la cellule officielle affectée est détruite l'utilisateur connecté est redirigé vers le clone de la cellule affecté qui est isolé dans le bateau PRISON.
Couper le lien, ne touche pas à la boîte, coupe juste le network puis clone la cellule vers PRISON et detruit la boite affectée qui est dans OFFICIER.
dès évasions d'un virus ou programme malveillant ou du mike-faux de sa cellule isolée vers le bateau PRISON le systeme genere un deuxieme bateau PRISON à l'état sain avant affectation clone toutes les cellules isolé dans la nouvelle prison sauf celle ou l'attaquant s'est évadé puis la cybercatographie actuel de la cellule de ce attaquant est envoyé dans le bateau SCIENCE puis l'ancien bateau de PRISON est détruite.
En cas d'affectation d'un bateau OFFICIEL genere un deuxieme bateau OFFICIEL clone à l'état sain avant affectation avec toutes les cellule sauf la cellule affecté puis la connexion SSH de ce client reste bloqué une alert est envoyé à l'entreprise client pour ce utilisateur la cellule affecté est cloné dans Prison une cellule clone à l'état sain avant affectation de ce client est genere dans OFFICIEL est les dix premières accèss SSH à cette nouvelle cellules doivent etre validées par double authentification, la premiere reconnexion doit etre validée par l'entreprise cliente.
La regeneration  à l'état sain précédent avant attaque MODELE, du bateau SCIENCE  en cas d'attaque.

# CYBERCARTOGRAPHIE, CYBERCARDS ET SIGNATURE SHA256

Une fois que bateau modele a acces aux deux autres bateaux, il creer des cybercard, des cybercartographies.
Par exemeple s'il y a une attaque, il cartographie l'attaque, il cartographie les recommandations, il cartographie la sécurité appliquée et il cartographie les actifs.
A la fin, le modele lui-même crée un cybercatographie.
Une fois qu'il y a attaque et isolation d'une cellule, considere une cellule est un conteneur, il genere la cybercatographie avant l'isolation de la cellule et il envoi dans le 4e bateau science cyber intelligent.
Une fois que le bateau modele a accs aux deux autres bateaux il crée des cybercards, des cybercartographie.
en cas d'attaque il cartographie l'attaque, catographie la sécurité appliqué et il cartographie les actifs.
Chaque cybercartographie est un document json modulaire et réutilisables découpé en quatres parties: cybercard attaque pour detaillé l'attaque le type et le vecteur d'entrée, cybercard actifs pour les fichiers et autres actifs z, cybercard securité pour la sécurité appliquée au moment de l'attaque, cybercard recommandation pour les actions à faire.
Chaque cybercard est signé avec un hash SHA256 au moment de sa création par le bateau MODELE.
Verification de signature côté bateau science, rejet si invalide.
Une fois que la cellule est dans le bateau PRISON, il récupère aussi les logs, comment se comporte le virus et tout, il crée aussi une cybercartographie après attaque là bas il y a aussi des nouvlles attaques qui apparaissent, des recommandations la sécuritéappliquée, la cartographie des actifs, il prend ça et il crée une deuxieme cartographie.
Dans cette cartographie il ajoute aussi la definition des objectifs des prochaines actions.

# BATEAU SCIENCE (THREAT-INTEL-LAB) ET BATEAU TEST

Il existe un 4e bateau: bateau science cyber intelligent qui est relié uniquement au bateau modèle.
Le bateau SCIENCE est pour la science cyber intelligent relier uniquement à bateau MODELE.
Bateau SCIENCE pour science cyber intelligente en technique c'est threat-intel-lab.
C'ets le container-4-science qui contient une base vectorielle Qdrant et le moteur d'apprentissage python.
Il est relié uniquement au bateau modélèle via un réseau docker interne internal true sans access internet, sans bridge vers l'exterieur.
Aucun autre container ne peur lui parler.
Communication via API interne exclusive entre container-3 et container-4.
Dans le bateau science cyber intelligence, il commence à créer des modèles, des cartes.
Ces modèles permettent de faire ressortir les futurs objectifsde sécurité, les futurs objectifs de sécyurité, les futurs objectifs de sécurité, les futures évaluations des menaces et des vulnérabilité, les futures méthodes pour déterminer les risques et définir les mesures de sécurité et leur mise en oeuvre.
Cette cybercartographie se découpe en plusieurs morceaux appelés cybercard.
Et avec ça il commence à s'entrainer pour proposer de nouvelles mesures de securité, de nouveaux schémas de sécurité.
il crée ça dans le bateau SCIENCE.
Le bateau SCIENCE fais ressortir des outils qui vont appliquer la sécurité, dont le script , des programmes du code qui va renforcer la sécurité actuelle des cellules et des cinq bateaux.
Il y a un test de la solution genere sur le bateau TEST apres test positif, il y a une demande humaine de l'admin de sécurité de l'entreprise client depuis local via VPN.
La regeneration à l'état initiale du bateau TEST apres tout tests.

# INTERFACE GRAPHIQUE ET VALIDATION HUMAINE DE SECURITE

Creer une application Web réact api backend connexion VPN SSH une cellule admin security  pour la validation humaine.
Par exemple s'il veut appliquer une recommandation, l'utilisateur à qui appartient la sécurité appui sur un bouton.
Il y a une app sur ce bouton.
Le bateau SCIENCE commence à classer les recommandations.
Si exemple il y a une recommandation et que l'utilisateur humain confirme, il applique.
Il prend le programme et il le deploie ce ecosysteme afin d'appliquer la nouvelle mesure de sécurité afin que prochainement on ne subisse plus la même attaque.
Une commande pour un deploiement sur VPS entreprise client et une autre pour deploiement sur VPS LAB.

# ECOSYSTEME MULTI-ENTREPRISES, ARCHITECTURE DU LAB CYBERSOCLE ET DISTRIBUTIONS DE VACCINS

Le VPS LAB appartient  l'équipe CYBERSOCLE confondateur OBIEY Christ Dany.
Chaque entreprise cliente possède son propre cloud SSH avec les cinq bateaux OFFICIEL PRISON MODELE SCIENCE TEST.
Le VPS LAB possèce également cinq bateaux OFFICIEL PRISON MODELE SCIENCE TEST.
Connexion VPN entre les bateaux PRISON-entreprises vers le bateau PRISON-LAB, les bateaux SCIENCE-entreprise avec le bateau SCIENCE-LAB, les bateaux TEST-entreprises avec le bateau TEST-LAB.
Les vacins generees par une entreprise  SCIENCES-entreprise testé positives sont envoyé vers le LAB retester si positif validation humaine de l'équipe de LAB puis envoyé aux autres entreprises si testé positif dans les entreprises respectifs demande de la validation humaine de chauqe entreprise.
Les attaques surveillé en temps reels PRISON-entreprises transferer dans LAB permettent à creer des vaccins dans SCIENCE-LAB.
Eviter la redondances des vaccins plus creer le nouveaux et ameliorer les anciens comme mise à jour.
Apres validation humaine de la version V2 donne la possibilité de repartir aux anciennes par exemple versions V1 V1.0.1 V1.0.2 .
