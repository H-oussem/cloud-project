import os

md_builder = """# ContainerLab — Guide d'Apprentissage, de Démo et de Soutenance

> **Projet :** ContainerLab — Conteneurisation et Orchestration locale vs Cloud (Proposition 2)  
> **Institution :** École Supérieure des Sciences et de la Technologie de Hammam Sousse (ESSTHS)  
> **Matière :** Virtualisation et Cloud Computing (2025–2026)  
> **Binôme :** Houssem Sassi & Nour El Houde Jaziri  
> **Enseignantes :** Mme Imen Nasr & Mme Maymouna Ben Said  
> **Version du livrable :** 1.0.0 — Document pédagogique complet de référence

---

## Sommaire
1. [Comment lire et utiliser ce guide](#1-comment-lire-et-utiliser-ce-guide)
2. [Le projet ContainerLab en 5 minutes](#2-le-projet-containerlab-en-5-minutes)
3. [Le pont complet avec le cours des professeures](#3-le-pont-complet-avec-le-cours-des-professeures)
4. [L'architecture expliquée simplement & en vrai code](#4-larchitecture-expliqu%C3%A9e-simplement--en-vrai-code)
5. [La démo pas à pas (Scénario chronométré 8 à 10 minutes)](#5-la-d%C3%A9mo-pas-%C3%A0-pas-sc%C3%A9nario-chronom%C3%A9tr%C3%A9-8-%C3%A0-10-minutes)
6. [Les 8 règles d'or d'ingénierie à connaître par cœur](#6-les-8-r%C3%A8gles-dor-ding%C3%A9nierie-%C3%A0-conna%C3%AEtre-par-c%C5%93ur)
7. [La suite de tests automatisée et ce qu'elle prouve vraiment](#7-la-suite-de-tests-automatis%C3%A9e-et-ce-quelle-prouve-vraiment)
8. [Les bugs réels rencontrés, pièges évités et leçons apprises](#8-les-bugs-r%C3%A9els-rencontr%C3%A9s-pi%C3%A8ges-%C3%A9vit%C3%A9s-et-le%C3%A7ons-apprises)
9. [Questions probables à la soutenance (18 Questions & Réponses percutantes)](#9-questions-probables-%C3%A0-la-soutenance-18-questions--r%C3%A9ponses-percutantes)
10. [Le grand glossaire en une phrase](#10-le-grand-glossaire-en-une-phrase)
11. [Checklist avant la soutenance & conseils pour le jour J](#11-checklist-avant-la-soutenance--conseils-pour-le-jour-j)

---

## 1. Comment lire et utiliser ce guide

Ce guide a été spécialement conçu pour vous permettre, à **Houssem Sassi** et **Nour El Houde Jaziri**, de maîtriser l'intégralité du projet **ContainerLab**, de comprendre en profondeur chaque ligne de configuration, d'établir un lien direct et inattaquable avec le cours théorique de **Mme Imen Nasr** et **Mme Maymouna Ben Said**, et de réussir votre soutenance orale avec la note maximale.

### Code Couleur & Système de Badges Pédagogiques
Tout au long de ce guide, des balises visuelles identifient immédiatement la nature des connaissances :
- `[COURS]` : Notion théorique issue directement des diapositives ou des travaux pratiques de l'ESSTHS.
- `[VALIDÉ EN LAB]` : Assertion technique vérifiée et validée par notre suite de tests automatisés.
- `[ATTENTION]` : Point de vigilance architecturale ou bonne pratique d'ingénierie.
- `[PIÈGE SOUTENANCE]` : Question piège fréquente des jurys et formulation recommandée pour y répondre sans hésiter.
- `[AWS]` : Équivalence avec les services de cloud public d'Amazon Web Services (EKS, ECS, ALB, RDS, VPC).

### Méthode de Travail Recommandée pour le Binôme
1. **Étape 1 (Compréhension globale) :** Lisez ensemble les Sections 2, 3 et 4 pour aligner votre vision d'ensemble du projet et son ancrage dans le cours.
2. **Étape 2 (Répétition de la démo) :** Répétez chronomètre en main la Section 5. Chaque membre doit connaître ses répliques et les commandes associées.
3. **Étape 3 (Questions/Réponses) :** Testez-vous mutuellement avec les 18 questions de la Section 9. L'un joue le rôle du professeur, l'autre répond sans notes.
4. **Étape 4 (Le Jour J) :** Suivez scrupuleusement la checklist de la Section 11 pour garantir un environnement de démonstration 100% opérationnel.

---

## 2. Le projet ContainerLab en 5 minutes

### Pourquoi ce projet ?
Le projet **ContainerLab** répond au sujet académique officiel **Proposition 2 : Conteneurisation et Orchestration locale vs Cloud**. Il matérialise la transition technologique majeure entre la virtualisation lourde par hyperviseur et la conteneurisation légère au niveau système d'exploitation.

Pour démontrer l'orchestration, nous avons développé une application 3-tiers moderne de gestion d'annonces d'ingénierie dotée d'une console d'observabilité interactive :
1. **Tier 1 (Frontend & Reverse Proxy) :** Single Page Application React 19 compilée avec Vite 6, servie par un serveur web Nginx Alpine ultra-léger (5.56 Mo).
2. **Tier 2 (API Backend) :** REST API haute performance développée avec Node.js 24 LTS et Express, s'exécutant sous utilisateur non-privilégié (`USER node`).
3. **Tier 3 (Base de Données) :** Base relationnelle PostgreSQL 16 Alpine persistée sur volume et initialisée automatiquement par schéma SQL.

### Synthèse des 3 Tiers Applicatifs

| Composant (Tier) | Technologies & Images | Rôle & Fonctionnalités | Sécurité & Réseau |
|---|---|---|---|
| **Tier 1 : Frontend & Reverse Proxy** | React 19 (Vite 6) servi par `nginx:stable-alpine-slim` | Délivre l'interface utilisateur, affiche l'observabilité du cluster, et relaie les requêtes `/api/*` vers le backend. | Exposé sur Port 3000 (Compose) ou Port 30080 (NodePort K8s). Seul point d'entrée externe du système. |
| **Tier 2 : Backend API** | Node.js 24 LTS + Express REST API | Exécute la logique métier, la validation stricte des entrées, les sondes de santé, et interroge la base PostgreSQL. | Exécution non-root (`USER node`). Port interne 5000. Invisible depuis l'extérieur du réseau de conteneurs. |
| **Tier 3 : Base de Données** | PostgreSQL 16 Alpine avec script `init.sql` | Assure le stockage persistant et relationnel des annonces et métadonnées système. | Port interne 5432. Isolée dans la DMZ `backend-net` (inaccessible au Frontend sous Docker Compose). |

### La Console d'Observabilité Interactive Intégrée
Le frontend intègre un tableau de bord d'observabilité réactif conçu sur mesure pour la soutenance :
- **Badge de Réplica Actif (Live Serving Replica) :** Interroge `GET /api/instance` pour afficher le nom d'hôte exact du conteneur ou Pod traitant la requête (ex: `api-7d498b58f9-k2x89`), avec un bouton de copie rapide pour le crash-test.
- **Indicateurs de Santé Temps Réel (Three-Tier Health Status) :** Feux tricolores surveillant le serveur web Nginx (:80), la vivacité de l'API (:5000) et la connectivité active au pool PostgreSQL (:5432).
- **Testeur de Répartition de Charge (Traffic Distribution) :** Envoie une rafale de 6 requêtes asynchrones en parallèle. L'interface affiche l'alternance des noms de Pods retournés, prouvant visuellement le load-balancing opéré par `kube-proxy`.
- **Fil d'Annonces Persistantes :** Permet de créer, valider et lister des annonces stockées en base relationnelle, servant de témoin infaillible pour les tests de persistance lors des redémarrages.

---

## 3. Le pont complet avec le cours des professeures

Cette section est la clé de voûte de votre préparation : elle établit une passerelle directe et systématique entre les notions enseignées en cours magistral par **Mme Imen Nasr** et **Mme Maymouna Ben Said** et leur réalisation concrète dans ContainerLab.

### 3.1 Virtualisation Matérielle vs Conteneurisation OS
- **Ce que le cours enseigne :** La virtualisation matérielle classique s'appuie sur un Hyperviseur (Type 1 bare-metal comme VMware ESXi/Hyper-V ou Type 2 hosted comme VirtualBox/VMware Workstation) pour émuler une machine physique complète. Chaque VM embarque son propre système d'exploitation invité (Guest OS), ce qui entraîne une consommation de stockage importante (plusieurs Go), une utilisation mémoire redondante et des temps de démarrage de plusieurs minutes. À l'inverse, la conteneurisation est une virtualisation au niveau du système d'exploitation qui ne virtualise pas le matériel mais crée des environnements isolés pour les processus en s'appuyant directement sur les fonctionnalités du noyau de l'hôte.
- **Ce que nous avons fait dans ContainerLab :** Nous avons éliminé toute émulation matérielle. Nos conteneurs (Frontend, API, Database) s'exécutent directement sur le noyau Linux de l'hôte (via Docker Engine / WSL2). Leurs images pèsent entre 5.56 Mo et 110 Mo, démarrent en moins de 2 secondes, et partagent efficacement le CPU et la RAM de l'hôte sans couche d'hyperviseur intermédiaire.

### 3.2 Les Fondations du Noyau Linux : chroot, cgroups et namespaces
Le cours explique que la conteneurisation repose historiquement sur trois briques fondamentales du noyau Linux :
1. **chroot (1979) :** Appel système qui modifie le répertoire racine perçu par un processus. Dans ContainerLab, chaque conteneur possède son propre système de fichiers racine isolé (`/usr/share/nginx/html`, `/app`, etc.), interdisant tout accès à l'arborescence de la machine hôte.
2. **cgroups (Control Groups, 2006) :** Mécanisme qui bride et mesure l'utilisation des ressources matérielles (CPU, mémoire, E/S). Dans `kubernetes/04-backend-deployment.yaml`, nous déclarons :
   ```yaml
   resources:
     requests: { memory: "128Mi", cpu: "100m" }
     limits:   { memory: "256Mi", cpu: "500m" }
   ```
   Grâce aux cgroups, un conteneur API qui s'emballerait est bridé à un demi-cœur CPU et 256 Mo de RAM, empêchant tout déni de service sur le nœud hôte.
3. **namespaces (2008) :** Partitionnent les ressources globales pour donner à chaque conteneur sa propre vue isolée :
   - `pid` : Numérotation des processus (le process Node.js s'exécute en tant que PID 1 dans son conteneur).
   - `net` : Interfaces et tables de routage propres (chaque conteneur a son adresse IP privée dédiée).
   - `mnt` : Points de montage de disques séparés.
   - `uts` : Nom d'hôte unique (ex: nom de Pod affiché sur le dashboard).
   - `user` : Mappage des privilèges (`USER node` UID 1000 au lieu de root).

### 3.3 De LXC à Docker & la Philosophie "Un Conteneur = Un Service"
LXC (2008) utilisait les cgroups et namespaces pour créer des conteneurs système s'apparentant à de petites VMs. Docker (2013) a révolutionné l'industrie en apportant :
1. La philosophie **"un conteneur = un service"** (découplage strict des responsabilités).
2. Le moteur `runc` communicant directement avec les APIs du noyau.
3. Le fichier déclaratif **Dockerfile**.
4. La distribution standardisée par **Images** et Registries (Docker Hub, ECR).

ContainerLab respecte scrupuleusement cette philosophie : 3 conteneurs spécialisés, découplés et facilement remplaçables.

### 3.4 Système de Fichiers Union (OverlayFS) et Multi-Stage Build
Une image Docker est un empilement de couches immuables (read-only layers). Au démarrage, Docker ajoute une couche supérieure inscriptible en Copy-on-Write (CoW).
Dans `application/frontend/Dockerfile`, nous exploitons cette mécanique avec un **Multi-Stage Build** :
- **Stage 1 (builder) :** Utilise `node:24-alpine` pour installer les dépendances et compiler le JSX avec Vite (`npm run build`).
- **Stage 2 (runner) :** Utilise `nginx:stable-alpine-slim`. Nous copions uniquement le dossier compilé `dist/` vers `/usr/share/nginx/html`.
- **Résultat mesuré (Test T02) :** L'image brute pesait **80.92 MB**. L'image finale de production ne pèse que **5.56 MB**, soit une réduction spectaculaire de **-93.1%** (-75.36 Mo d'outils inutiles éliminés !).

### 3.5 Réseau Virtuel : Bridging, NAT et Host-Only vs Docker & Kubernetes
Le cours de virtualisation détaille trois modes de mise en réseau de VMs :
1. **Bridge (Pont) :** La VM obtient une IP sur le réseau physique local comme un équipement physique.
2. **NAT (Traduction d'adresses) :** L'hyperviseur masque la VM derrière l'IP de l'hôte et translate les ports.
3. **Host-Only (Hôte uniquement) :** Réseau privé isolé accessible uniquement entre l'hôte et les VMs.

Dans ContainerLab :
- **Sous Docker Compose :** Docker crée deux commutateurs virtuels bridge (`frontend-net` et `backend-net`). Les conteneurs communiquent par leur nom DNS interne. L'accès externe se fait par redirection NAT de port (`-p 3000:80`).
- **Sous Kubernetes :** Chaque Pod reçoit une IP routable unique dans le cluster (modèle IP-par-Pod). Le composant `kube-proxy` configure des règles `iptables` pour diriger le trafic des Services ClusterIP vers les réplicas sains. Le service `NodePort` (port 30080) fait le pont avec l'hôte physique.

### 3.6 Persistance du Stockage : Éphémère vs Volumes & PVC
Par défaut, le stockage d'un conteneur est éphémère : si le conteneur est détruit, sa couche inscriptible est purgée.
- **Sous Docker Compose :** Un volume nommé géré (`postgres_data`) est monté dans `/var/lib/postgresql/data`.
- **Sous Kubernetes :** Nous utilisons le standard en deux temps :
  1. `PersistentVolumeClaim` (PVC `postgres-pvc`, 1 Gi, mode `ReadWriteOnce`).
  2. Le contrôleur de stockage Minikube (`k8s.io/minikube-hostpath`) provisionne dynamiquement le PersistentVolume (`PV`) et le lie (`Bound`).
  3. Le Pod monte ce PVC : même si le Pod est détruit, le nouveau Pod se reconnecte au même disque sans perte d'octets.

### 3.7 Modèles de Service & Déploiement Cloud
- **Modèles de Service :**
  - **IaaS (Infrastructure as a Service) :** LAB-01 EC2 (gestion manuelle de l'OS, des patchs, de la configuration Apache).
  - **CaaS / PaaS (Container / Platform as a Service) :** ContainerLab, Docker, AWS EKS, AWS ECS Fargate (le développeur livre son conteneur déclaratif, le cloud gère le runtime).
  - **SaaS (Software as a Service) :** Application prête à l'emploi (ex: Google Drive, Notion).
- **Modèles de Déploiement :**
  - **Cloud Privé / Local :** Minikube et Docker Compose sur la machine de développement.
  - **Cloud Public :** Déploiement sur AWS (EKS / ECS / RDS).
  - **Cloud Hybride :** Développement local sous Minikube et synchronisation de production vers AWS.

### 3.8 L'Étude de Cas Wikileaks (Cours de Cloud Computing)
Le cours de Mme Imen Nasr analyse l'incident de décembre 2010 où Wikileaks a subi une attaque DDoS massive (>10 Gbps) puis une rupture contractuelle de la part d'Amazon AWS, contraignant le site à migrer en urgence vers des serveurs OVH en France et le réseau P2P BitTorrent.
Ce cas enseigne deux leçons fondamentales appliquées à ContainerLab :
1. **Élasticité dynamique :** Capacité d'augmenter instantanément les réplicas face à une hausse de charge (`kubectl scale deployment api --replicas=4`).
2. **Portabilité sans enfermement propriétaire (No Vendor Lock-in) :** Les conteneurs Docker OCI et les manifestes Kubernetes sont strictement portables : ils s'exécutent à l'identique sur un PC portable, sur AWS, Google Cloud, Azure ou un datacenter privé sans réécrire une seule ligne de code.

### 3.9 Algorithme Sandpiper vs Kubernetes Control Plane
Le cours de virtualisation présente **Sandpiper**, un système de gestion automatisée de machines virtuelles qui surveille les métriques physiques (CPU, réseau, mémoire) et atténue les surcharges ("hotspots") par migration à chaud de VMs.
Dans Kubernetes, cette logique est nativement intégrée :
- Le `kube-scheduler` place intelligemment les Pods sur les nœuds disposant des ressources suffisantes (`requests`).
- Le `Horizontal Pod Autoscaler` (HPA) surveille l'utilisation des cgroups et augmente automatiquement les réplicas.
- Le `kube-controller-manager` réconcilie en permanence l'état désiré et l'état observé.

### 3.10 Correspondance Directe avec les Travaux Pratiques AWS
- **LAB-01 (AWS EC2) :**
  - Instance EC2 Linux -> Conteneur Docker (Frontend / Backend).
  - Security Groups -> Ports exposés et règles de routage bridge.
  - Paire de clés SSH -> Authentification par clé/token.
  - User Data script -> Directives `RUN` et scripts `init.sql`.
- **LAB-02 (AWS VPC) :**
  - VPC 10.0.0.0/16 -> Réseau de conteneurs interne.
  - Subnet Public + Internet Gateway (IGW) -> Réseau `frontend-net` exposé sur le port hôte.
  - Subnet Privé + NAT Gateway -> Réseau `backend-net` et base PostgreSQL isolée d'Internet.
  - Security Groups inter-tiers -> Cloisonnement Nginx -> API -> PostgreSQL.

### 3.11 Architecture Kubernetes : Control Plane vs Worker Nodes
- **Control Plane (Cerveau) :** `kube-apiserver` (point d'entrée REST), `etcd` (base clé-valeur d'état), `kube-scheduler` (placement des Pods), `kube-controller-manager` (boucles de réconciliation).
- **Worker Node (Exécutant) :** `kubelet` (pilote du nœud), `kube-proxy` (routage réseau et load-balancing), container runtime (`docker` / `containerd`).

---

## 4. L'architecture expliquée simplement & en vrai code

### 4.1 Le Parcours d'une Requête HTTP de A à Z
Lorsqu'un utilisateur consulte ou publie une annonce :
1. Le navigateur web interroge l'URL externe `http://localhost:3000` (Compose) ou `http://<minikube-ip>:30080` (K8s).
2. Le serveur **Nginx** intercepte la requête :
   - Si l'URL correspond à `/`, il sert directement les fichiers HTML/JS/CSS statiques mis en cache.
   - Si l'URL commence par `/api/*`, Nginx agit en **Reverse Proxy** et transfère le paquet vers le service interne `http://api:5000/api/*`.
3. Le **Load Balancer** (`kube-proxy` en mode iptables) sélectionne l'un des Pods API sains en Round-Robin.
4. Le processus **Node.js Express** :
   - Ajoute l'en-tête de traçabilité `X-Served-By: <hostname>`.
   - Valide les données JSON entrantes (titre non vide, longueur <= 150 caractères).
   - Exécute la requête SQL paramétrée (`INSERT INTO announcements...`) via le pool `pg`.
5. La base **PostgreSQL 16** valide la transaction ACID, persiste la ligne sur son volume persistant et renvoie le tuple inséré.
6. La réponse HTTP 201 est retournée au navigateur et l'interface utilisateur React met à jour le DOM sans rechargement de page.

### 4.2 Pourquoi le Reverse Proxy Nginx est indispensable
Sans reverse proxy, l'application React exécutée dans le navigateur de l'ordinateur portable de l'enseignant tenterait d'interroger directement `http://api:5000`. Or :
1. Le navigateur de l'hôte physique ne peut pas résoudre les noms DNS internes du cluster (`api` ou `postgres`).
2. Cela provoquerait une erreur fatale `ERR_NAME_NOT_RESOLVED`.
3. De plus, cela nécessiterait d'activer le partage CORS et d'exposer publiquement le backend.
En plaçant Nginx en frontal, le frontend et l'API partagent la même origine (`same-origin`), garantissant **zéro problème de CORS** et une sécurité renforcée.

### 4.3 La DMZ bi-réseau et la Sécurité Réseau
Dans `compose.yaml`, nous déclarons deux sous-réseaux isolés :
- `frontend-net` : Connecte le conteneur Frontend et le conteneur API.
- `backend-net` : Connecte le conteneur API et le conteneur Database.
Le conteneur Frontend ne participe pas au réseau `backend-net`. Même si un assaillant parvenait à compromettre le serveur web Nginx, il lui est physiquement impossible de joindre le port 5432 de la base de données.

### 4.4 L'Exécution Non-Root
Dans `application/backend/Dockerfile`, nous déclarons :
```dockerfile
USER node
```
Par défaut, un processus dans un conteneur tourne avec l'UID 0 (`root`). Si une vulnérabilité permet de s'échapper du conteneur (container breakout), l'assaillant deviendrait immédiatement root sur la machine hôte. En basculant sur l'utilisateur `node` (UID 1000), nous appliquons le **principe du moindre privilège**.

### 4.5 Gestion des Secrets et Paramètres Externes
Aucun mot de passe ni chaîne de connexion n'est écrit en dur dans le code source :
- Les paramètres non-sensibles sont injectés via une **ConfigMap** (`01-api-configmap.yaml` : ports, host, log level).
- Les identifiants sensibles sont stockés dans un **Secret** Kubernetes encodé en base64 (`02-api-secret.yaml` : mot de passe PostgreSQL).

---

## 5. La démo pas à pas (Scénario chronométré 8 à 10 minutes)

### Rôles du Binôme
- **Houssem Sassi :** Présentation générale, démonstration Docker Compose, benchmarks d'optimisation (-93.1%), crash-tests (auto-guérison API et persistance de la base).
- **Nour El Houde Jaziri :** Déploiement Kubernetes, manifestes déclaratifs, dashboard d'observabilité, démonstration du scaling horizontal (2 à 4 réplicas) et projection cloud AWS.

### Scénario Minute par Minute

#### Étape 1 : Cadrage Académique & Objectif (0:00 - 1:00 · Houssem)
- **Action :** Afficher le README ou la console d'accueil ContainerLab.
- **Discours :** *"Bonjour Madame. Dans le cadre du cours de Virtualisation et Cloud Computing, nous présentons la Proposition 2 : Conteneurisation et Orchestration locale vs Cloud. ContainerLab matérialise le passage de la virtualisation lourde à la conteneurisation légère via une application 3-tiers résiliente (React, Node.js Express, PostgreSQL). Nous allons vous démontrer son orchestration sous Docker Compose puis sous Kubernetes sur Minikube, validée par notre matrice de tests T01 à T11."*

#### Étape 2 : Démonstration Docker Compose & Isolation DMZ (1:00 - 2:30 · Houssem)
- **Action :** Exécuter `.\scripts\run-compose.ps1` puis `docker compose ps`.
- **Preuve visuelle :** Les 3 conteneurs affichent `Up (healthy)`.
- **Discours :** *"Sous Docker Compose, nous avons configuré deux réseaux bridge isolés : frontend-net et backend-net. L'API est la seule passerelle entre les deux. La base de données PostgreSQL est totalement inaccessible depuis l'extérieur et depuis le frontend. De plus, nos dépendances sont synchronisées par des sondes de santé (condition: service_healthy) : l'API attend que la base soit prête avant de démarrer."*

#### Étape 3 : Benchmarks d'Optimisation des Dockerfiles (2:30 - 3:30 · Houssem)
- **Action :** Exécuter `.\scripts\benchmark-images.ps1` ou ouvrir `docs/benchmarks/image-sizes.md`.
- **Preuve visuelle :** Tableau montrant la réduction de l'image Frontend de 80.92 Mo à 5.56 Mo (-93.1%).
- **Discours :** *"Pour répondre à l'axe 1 du barème, nous avons conçu des Dockerfiles de production. Pour le frontend, notre Multi-Stage Build utilise Node 24 pour la compilation puis copie les fichiers statiques dans Nginx Alpine. Résultat : une réduction de 93.1% de la taille d'image (-75 Mo d'outils inutiles éliminés). Côté backend, nous appliquons USER node pour interdire l'exécution root."*

#### Étape 4 : Déploiement Déclaratif Kubernetes sur Minikube (3:30 - 4:45 · Nour)
- **Action :** Exécuter `.\scripts\deploy-k8s.ps1` puis `kubectl get all,pvc -n containerlab`.
- **Preuve visuelle :** Namespace créé, PVC en statut `Bound`, Pods en statut `Running (1/1 Ready)`.
- **Discours :** *"Nous passons à l'orchestration de cluster avec Kubernetes. Nous appliquons 10 manifestes déclaratifs numérotés de 00 à 09. Nous isolons notre application dans le Namespace containerlab. La configuration et les secrets sont découplés via ConfigMap et Secret. Les briques internes communiquent par Services ClusterIP, tandis que le frontend est exposé à l'extérieur par un Service NodePort sur le port 30080."*

#### Étape 5 : Navigation sur le Dashboard & Test Inter-Tiers (4:45 - 6:00 · Nour)
- **Action :** Basculer sur le navigateur web. Constater les 3 feux verts. Publier une annonce *"Test Soutenance ESSTHS 2026"*.
- **Preuve visuelle :** L'annonce s'affiche immédiatement. Le badge `Serving Replica` affiche le nom du Pod API qui a traité la requête.
- **Discours :** *"Voici notre console d'observabilité. Elle interroge l'endpoint /api/instance pour afficher en direct le Pod Kubernetes traitant la requête. La création de l'annonce prouve le bon fonctionnement de la chaîne 3-tiers : le navigateur a interrogé Nginx, qui a relayé à l'API via ClusterIP, qui a validé et persisté la donnée dans PostgreSQL."*

#### Étape 6 : MOMENT FORT 1 — Équilibrage de Charge & Scaling Horizontal (6:00 - 7:00 · Nour)
- **Action :** Cliquer sur le bouton *"Tester la distribution de trafic"* sur l'interface (rafale de 6 requêtes). Dans le terminal : `kubectl scale deployment api --replicas=4 -n containerlab`.
- **Preuve visuelle :** L'interface affiche l'alternance des réplicas (load balancing Round-Robin). Le terminal montre le passage instantané de 2 à 4 réplicas en moins de 3 secondes.
- **Discours :** *"C'est notre premier moment fort : l'élasticité horizontale. kube-proxy répartit équitablement le trafic entre les Pods disponibles. En augmentant la consigne à 4 réplicas, le ReplicaSet instancie immédiatement deux nouveaux Pods. Dès que leur sonde de préparation (readinessProbe) répond avec succès, ils rejoignent le pool de routage."*

#### Étape 7 : MOMENT FORT 2 — Crash-Test d'Auto-Guérison (7:00 - 8:00 · Houssem)
- **Action :** Copier le nom du Pod actif affiché sur le dashboard, puis dans le terminal :
  ```bash
  kubectl delete pod <nom-du-pod-actif> -n containerlab --now
  ```
- **Preuve visuelle :** Dans le terminal surveillant les Pods, le Pod passe en `Terminating` et un nouveau Pod est créé en moins de 2 secondes. Le dashboard continue de fonctionner sans aucune interruption de service.
- **Discours :** *"Deuxième moment fort : la résilience par auto-guérison (self-healing). Nous venons d'abattre brutalement le Pod API qui répondait à nos requêtes. La boucle de réconciliation du ReplicaSet détecte immédiatement l'écart entre l'état désiré (4) et l'état réel (3) et lance un remplaçant. Le service ne subit aucune seconde d'interruption."*

#### Étape 8 : MOMENT FORT 3 — Persistance des Données après Crash de la Base (8:00 - 9:00 · Houssem)
- **Action :** Supprimer brutalement le Pod PostgreSQL :
  ```bash
  kubectl delete pod -l app=postgres -n containerlab --now
  ```
  Attendre 4 secondes que le contrôleur recrée le Pod, puis rafraîchir la page web.
- **Preuve visuelle :** L'annonce créée à l'Étape 5 est toujours présente dans la liste !
- **Discours :** *"Troisième moment fort : la gestion du stockage persistant (Axe 4 du barème). Les conteneurs sont éphémères, mais pas notre stockage : grâce au PersistentVolumeClaim et à notre stratégie Recreate, le nouveau Pod PostgreSQL s'est reconnecté au même volume persistant sans conflit de verrouillage. Zéro perte de données !"*

#### Étape 9 : Projection Cloud d'Entreprise AWS & Comparaison ECS (9:00 - 9:45 · Nour)
- **Action :** Projeter le schéma d'architecture AWS de `docs/aws-comparison.md`.
- **Preuve visuelle :** Diagramme VPC Multi-AZ avec ALB, EKS / ECS Fargate et RDS Multi-AZ.
- **Discours :** *"Pour déployer ContainerLab en production sur AWS, nous transposerions nos briques : Minikube devient Amazon EKS ou Amazon ECS avec AWS Fargate sans serveur. Notre NodePort devient un Application Load Balancer (ALB) avec certificat SSL et AWS WAF. Et pour la base, au lieu d'un conteneur avec PVC, la bonne pratique cloud est d'utiliser Amazon RDS PostgreSQL managé avec réplication synchrone Multi-AZ et basculement automatique en moins de 60 secondes."*

#### Étape 10 : Conclusion & Ouverture aux Questions (9:45 - 10:00 · Binôme)
- **Discours :** *"En conclusion, ContainerLab valide l'ensemble des compétences de la Proposition 2 : Dockerfiles optimisés (-93%), composition sécurisée en DMZ, déploiement déclaratif sur Kubernetes, scalabilité horizontale, self-healing et persistance sans faille. Nous vous remercions pour votre écoute et nous sommes prêts à répondre à vos questions."*

### Plan B : Que faire si un incident survient pendant la démo ?

| Incident Possible | Cause Probable | Solution Immédiate (< 10 secondes) |
|---|---|---|
| **Port 3000 déjà utilisé** | Une ancienne instance de Compose ou process Node tourne. | Exécuter `.\scripts\cleanup.ps1` puis relancer `.\scripts\run-compose.ps1`. |
| **Minikube ne répond pas** | Cluster en pause ou Docker Desktop redémarré. | Exécuter `minikube status`. Si éteint, lancer `minikube start --driver=docker`. |
| **Erreur ImagePullBackOff** | Images non chargées dans le cache de Minikube. | Lancer immédiatement `.\scripts\load-images.ps1` (charge les images locales hors-ligne). |
| **La base met du temps à démarrer** | PostgreSQL initialise le volume (`init.sql`). | Montrer la sonde `/api/health/ready` qui renvoie 503 : expliquer que le découplage protège le cluster ! |

---

## 6. Les 8 règles d'or d'ingénierie à connaître par cœur

1. **Règle 1 : Multi-Stage Build obligatoire pour les applications compilées.**  
   *Justification :* Divise la taille d'image par 14 (-93.1%) et élimine les compilateurs de production, réduisant la surface d'attaque.
2. **Règle 2 : Stratégie `Recreate` impérative sur PostgreSQL avec volume `ReadWriteOnce`.**  
   *Justification :* Empêche l'erreur fatale `Multi-Attach error for volume` qui survient avec la stratégie par défaut `RollingUpdate`.
3. **Règle 3 : Découpler la sonde de vivacité (`livenessProbe`) de la sonde de préparation (`readinessProbe`).**  
   *Justification :* Si PostgreSQL redémarre, l'API ne doit pas être redémarrée par Kubernetes (`liveness`), mais simplement retirée du pool de routage (`readiness`).
4. **Règle 4 : Politique `imagePullPolicy: Never` et tags sémantiques stricts en évaluation locale.**  
   *Justification :* Empêche Kubernetes d'interroger Docker Hub pour des images locales et garantit l'indépendance réseau.
5. **Règle 5 : Exécution non-root (`USER node`) pour le principe de moindre privilège.**  
   *Justification :* Empêche qu'une compromission applicative n'octroie les privilèges root sur la machine hôte.
6. **Règle 6 : Le Namespace est une frontière administrative, pas un pare-feu réseau.**  
   *Justification :* Les Namespaces isolent les noms d'objets. L'isolation réseau nécessite des `NetworkPolicies`.
7. **Règle 7 : `condition: service_healthy` dans Compose pour un ordonnancement déterministe.**  
   *Justification :* `depends_on` classique ne vérifie que le démarrage du conteneur. `service_healthy` attend que la base réponde à `pg_isready`.
8. **Règle 8 : Service NodePort 30080 pour l'indépendance vis-à-vis des contrôleurs cloud.**  
   *Justification :* Sur Minikube local, un Service `LoadBalancer` reste en `<pending>` sans contrôleur externe. NodePort fonctionne partout.

---

## 7. La suite de tests automatisée et ce qu'elle prouve vraiment

### 7.1 Les Tests Unitaires Node.js (`test/api.test.js`)
Exécutés avec le module natif `node:test` (zéro dépendance externe) :
- **Test 1 :** `GET /api/health/live` renvoie HTTP 200 et `status: alive`.
- **Test 2 :** `GET /api/health/ready` renvoie HTTP 200 quand la base répond, ou HTTP 503 si la base est inaccessible.
- **Test 3 :** `GET /api/instance` renvoie le nom d'hôte de la machine/Pod.
- **Test 4 :** `POST /api/announcements` sans titre renvoie HTTP 400 et un message d'erreur clair.
- **Test 5 :** `POST /api/announcements` avec un titre > 150 caractères est rejeté avec HTTP 400.
- **Test 6 :** `GET /api/announcements?limit=invalide` est rejeté avec HTTP 400.
- **Test 7 :** Route inexistante (`GET /api/inconnue`) renvoie HTTP 404.

### 7.2 Matrice d'Orchestration End-to-End : Tests T01 à T11

| ID | Niveau | Scénario Testé | Procédure & Commande | Résultat Validé |
|---|---|---|---|---|
| **Unit** | Applicatif | Validation unitaire API Express | `npm test` dans `application/backend` | 7/7 réussis (Code 0) |
| **T01** | Build | Construction des images multi-stage | `.\scripts\build-images.ps1` | 3 images v1.0.0 créées |
| **T02** | Optimisation | Benchmark d'optimisation d'image | `.\scripts\benchmark-images.ps1` | -93.1% Frontend (5.56 Mo) |
| **T03** | Compose | Orchestration locale multi-services | `.\scripts\run-compose.ps1` | 3 services healthy |
| **T04** | Compose | Communication inter-tiers (CRUD) | Insertion REST `POST /api/announcements` | HTTP 201 Donnée stockée |
| **T05** | Compose | Persistance du volume nommé | `docker compose restart postgres` | Donnée préservée au reboot |
| **T06** | K8s | Déploiement déclaratif complet | `.\scripts\deploy-k8s.ps1` | 4 Pods Running, PVC Bound |
| **T07** | K8s | Équilibrage de charge (Load Balancing) | 10 requêtes consécutives à `/api/instance` | 2 Pods alternés (6 et 4) |
| **T08** | K8s | Scaling horizontal des réplicas | `kubectl scale deployment api --replicas=4` | 4 réplicas Ready |
| **T09** | K8s | Auto-guérison (Self-Healing) | `kubectl delete pod <api-pod> --now` | Pod recréé en < 2s |
| **T10** | K8s | Persistance du PVC PostgreSQL | `kubectl delete pod <postgres-pod> --now` | Données intactes au reboot |
| **T11** | Cleanup | Démontage propre de l'infrastructure | `.\scripts\cleanup.ps1` | Cluster propre (Code 0) |

---

## 8. Les bugs réels rencontrés, pièges évités et leçons apprises

| Symptôme / Erreur | Cause Technique Profonde | Correction Appliquée | Leçon d'Ingénierie |
|---|---|---|---|
| **Multi-Attach error for volume** lors de la mise à jour de PostgreSQL | Le volume persistant Minikube est `ReadWriteOnce`. Avec la stratégie par défaut `RollingUpdate`, le nouveau Pod tente de monter le disque alors que l'ancien le détient encore. | Configuration explicite de `strategy: { type: Recreate }` dans `04-database-deployment.yaml`. | Un volume RWO ne peut avoir qu'un seul montage en écriture à la fois : toujours éteindre avant de remonter. |
| **ERR_NAME_NOT_RESOLVED** sur les appels `http://api:5000` | Le code JavaScript React tourne dans le navigateur de l'hôte Windows. L'hôte ne peut pas résoudre les noms DNS internes du réseau de conteneurs. | Configuration d'un reverse proxy dans Nginx (`location /api/ { proxy_pass http://api:5000/api/; }`). | Ne jamais exposer de noms DNS internes aux clients web : toujours passer par une passerelle inverse (Reverse Proxy). |
| **ErrImagePull / ImagePullBackOff** sur Minikube | Kubernetes utilise par défaut le tag `latest` avec `imagePullPolicy: Always`, interrogeant Docker Hub qui ne possède pas nos images locales. | Attribution de tags sémantiques stricts (`v1.0.0`), préchargement via `minikube image load` et politique `imagePullPolicy: Never`. | En environnement de test local, forcer l'usage des images locales pour garantir l'indépendance réseau. |
| **Crash en boucle de PostgreSQL (Exit code 1)** | Tentative initiale d'exécuter PostgreSQL avec un utilisateur non-root sans permissions sur `/var/lib/postgresql/data`. | Utilisation de l'image officielle PostgreSQL Alpine qui gère ses propres permissions internes via son entrypoint. | Ne pas surcharger aveuglément l'utilisateur sur les images de bases de données officielles sans adapter les ACLs du volume. |
| **Reboot en cascade des Pods API** | La sonde de vivacité (`livenessProbe`) vérifiait la connectivité à PostgreSQL (`SELECT 1`). Lors d'un restart temporaire de la base, K8s tuait tous les Pods API sains. | Séparation stricte : `/api/health/live` vérifie uniquement l'API, `/api/health/ready` vérifie la base. | Une sonde de vivacité ne doit JAMAIS dépendre d'un tiers externe sous peine de provoquer un effondrement en cascade. |
| **Conflit de port hôte 5432** | Une instance PostgreSQL locale tournait déjà sur la machine Windows de l'étudiant. | Suppression du mapping de port hôte pour PostgreSQL sous Compose (accès exclusif via le réseau interne `backend-net`). | Ne mapper sur l'hôte physique que les services strictement destinés aux utilisateurs finaux. |
| **Fichiers statiques 404 lors du rafraîchissement d'une sous-page** | Nginx ne trouvait pas de fichier correspondant à la route dynamique de la SPA React. | Ajout de la directive `try_files $uri $uri/ /index.html;` dans `nginx.conf`. | Dans toute SPA, le serveur web doit rediriger toutes les routes non trouvées vers `index.html`. |
| **Échec du build Docker sur Windows (fins de ligne CRLF)** | Les scripts shell d'initialisation contenaient des retours chariot Windows (`\r\n`), rejetés par le kernel Linux d'Alpine. | Configuration de Git (`.gitattributes`) pour forcer les fins de ligne Unix (`LF`) sur tous les scripts et Dockerfiles. | Toujours imposer les fins de ligne `LF` dans un projet destiné à tourner sous conteneur Linux. |

---

## 9. Questions probables à la soutenance (18 Questions & Réponses percutantes)

### Q01 : Quelle est la différence fondamentale entre la virtualisation et la conteneurisation ?
**Réponse modèle :** La virtualisation matérielle utilise un hyperviseur pour émuler du matériel et faire tourner des OS invités complets avec leur propre noyau (lourd, plusieurs Go, démarrage en minutes). La conteneurisation est une virtualisation au niveau du système d'exploitation : elle partage le noyau unique de l'hôte et isole les processus via les cgroups et les namespaces (léger, quelques Mo, démarrage en secondes).  
*📁 Référence : Diapositives Conteneurisation (p. 4-7) & Chapitre02-Virtualisation (p. 4-7).*

### Q02 : Quels sont les mécanismes du noyau Linux qui rendent les conteneurs possibles ?
**Réponse modèle :** Trois mécanismes fondamentaux :
1. **chroot :** Isole le système de fichiers racine du processus.
2. **cgroups (Control Groups) :** Brident et comptabilisent l'usage des ressources physiques (CPU, RAM, E/S).
3. **namespaces :** Partitionnent la vue du système (PID pour les processus, NET pour le réseau, MNT pour les disques, UTS pour le hostname, USER pour les identifiants).  
*📁 Référence : Diapositives Conteneurisation (p. 10-13).*

### Q03 : Comment fonctionne le Multi-Stage Build et quel gain avez-vous obtenu ?
**Réponse modèle :** Le Multi-Stage Build utilise plusieurs instructions `FROM` dans un unique Dockerfile. Le premier stage installe les outils de build volumineux (Node.js 24, Vite, npm) et compile le code. Le second stage démarre d'une image d'exécution minimale (`nginx:stable-alpine-slim`) et copie uniquement les fichiers compilés du premier stage. Dans ContainerLab, nous avons réduit l'image frontend de 80.92 Mo à 5.56 Mo, soit un gain mesuré de **-93.1%**.  
*📁 Référence : `application/frontend/Dockerfile` & `docs/benchmarks/image-sizes.md`.*

### Q04 : Pourquoi utiliser un Reverse Proxy Nginx plutôt que d'appeler l'API directement depuis React ?
**Réponse modèle :** Deux raisons critiques :
1. Le code React s'exécute dans le navigateur de l'ordinateur hôte. L'hôte physique ne peut pas résoudre le DNS interne du conteneur `api:5000` (erreur `ERR_NAME_NOT_RESOLVED`).
2. En faisant relayer les requêtes `/api/*` par Nginx sur le même port d'écoute, le frontend et le backend partagent la même origine web (`same-origin`), éliminant tout blocage de sécurité CORS.  
*📁 Référence : `application/frontend/nginx.conf`.*

### Q05 : Comment avez-vous sécurisé les réseaux sous Docker Compose ?
**Réponse modèle :** Nous avons créé une Zone Démilitarisée (DMZ) avec deux réseaux bridge distincts : `frontend-net` et `backend-net`. Le frontend et l'API sont sur `frontend-net`, l'API et la base sont sur `backend-net`. La base de données PostgreSQL ne possède aucune interface sur `frontend-net` et n'expose aucun port sur la machine hôte : elle est totalement inaccessible au navigateur et au serveur web.  
*📁 Référence : `compose.yaml` (lignes 6-35).*

### Q06 : Pourquoi exécuter l'API sous un utilisateur non-root (`USER node`) ?
**Réponse modèle :** Par défaut, un conteneur tourne avec les privilèges root (UID 0). En cas de vulnérabilité applicative avec évasion de conteneur (container escape), l'assaillant obtiendrait les privilèges root sur la machine hôte. En basculant sur l'utilisateur `node` (UID 1000), nous appliquons le principe du moindre privilège pour confiner l'impact d'une éventuelle faille.  
*📁 Référence : `application/backend/Dockerfile` (ligne 18).*

### Q07 : Pourquoi avoir séparé la sonde de vivacité (`livenessProbe`) et la sonde de préparation (`readinessProbe`) ?
**Réponse modèle :** La sonde de vivacité `/api/health/live` vérifie uniquement si le processus Node.js tourne. Si elle échoue, Kubernetes redémarre le Pod. La sonde de préparation `/api/health/ready` vérifie si PostgreSQL est joignable. Si la base subit une coupure temporaire, l'API échoue à la préparation et Kubernetes cesse simplement de lui envoyer du trafic sans redémarrer le conteneur en boucle. Cela évite un effondrement en cascade du cluster.  
*📁 Référence : `kubernetes/04-backend-deployment.yaml` & `docs/decision-log.md` (ADR-005).*

### Q08 : Pourquoi avoir configuré `strategy: Recreate` sur le déploiement de la base de données ?
**Réponse modèle :** Notre volume persistant Minikube est de type `ReadWriteOnce` (montable par un seul nœud à la fois). Avec la stratégie par défaut `RollingUpdate`, Kubernetes démarre le nouveau Pod avant de tuer l'ancien. Le nouveau Pod tente de monter le volume encore verrouillé, provoquant une erreur `Multi-Attach error for volume`. La stratégie `Recreate` détruit d'abord l'ancien Pod pour libérer le volume avant de lancer le nouveau.  
*📁 Référence : `kubernetes/03-database-deployment.yaml` & `docs/decision-log.md` (ADR-002).*

### Q09 : Quelle est la différence entre un PersistentVolume (PV) et un PersistentVolumeClaim (PVC) ?
**Réponse modèle :** Le PV représente la ressource de stockage physique concrète provisionnée par l'administrateur ou le fournisseur de cloud. Le PVC est la requête ou réservation émise par le développeur (taille demandée, mode d'accès). C'est le même principe que pour le calcul : un Pod demande du CPU/RAM, un PVC demande du stockage.  
*📁 Référence : Diapositives Conteneurisation (p. 42-45) & `kubernetes/03-database-pvc.yaml`.*

### Q10 : Pourquoi utiliser `imagePullPolicy: Never` sur Minikube ?
**Réponse modèle :** Par défaut avec un tag personnalisé, Kubernetes utilise la politique `Always` qui contacte les registres externes (Docker Hub). Comme nos images sont construites localement et préchargées dans le démon Minikube (`minikube image load`), la politique `Never` force Kubernetes à utiliser exclusivement le cache local, garantissant un déploiement 100% hors-ligne sans risque d'erreur `ErrImagePull`.  
*📁 Référence : `kubernetes/04-backend-deployment.yaml` & `docs/decision-log.md` (ADR-003).*

### Q11 : Comment fonctionne l'équilibrage de charge (Load Balancing) dans Kubernetes ?
**Réponse modèle :** Le Service Kubernetes (ClusterIP) attribue une adresse IP virtuelle stable et un nom DNS interne. Sur chaque nœud, le composant `kube-proxy` configure des règles `iptables` ou IPVS. Lorsqu'une requête arrive, `kube-proxy` traduit l'IP virtuelle du service vers l'une des adresses IP réelles des Pods sains rattachés (EndPoints) selon un algorithme Round-Robin.  
*📁 Référence : Diapositives Conteneurisation (p. 36-39).*

### Q12 : Pourquoi utiliser un Service NodePort (30080) plutôt qu'un Service LoadBalancer ?
**Réponse modèle :** Le type `LoadBalancer` nécessite un contrôleur d'équilibrage fourni par un cloud public (ex: AWS NLB/ALB). Sur un cluster Minikube local standard, un service `LoadBalancer` reste indéfiniment en statut `<pending>`. Le `NodePort` ouvre un port statique dédié (entre 30000 et 32767) sur toutes les interfaces du cluster, fonctionnant de manière autonome sans dépendance cloud.  
*📁 Référence : `kubernetes/05-frontend-service.yaml`.*

### Q13 : Quelle est la différence entre un Namespace Kubernetes et une NetworkPolicy ?
**Réponse modèle :** Un Namespace est une frontière purement logique et administrative qui partitionne les noms d'objets et permet d'appliquer des quotas de ressources. Il n'isole pas le trafic réseau : par défaut, un Pod d'un namespace peut contacter un Pod d'un autre namespace. Pour restreindre le trafic réseau, il faut obligatoirement configurer des `NetworkPolicies`.  
*📁 Référence : Diapositives Conteneurisation (p. 34).*

### Q14 : Que se passe-t-il exactement lorsqu'un Pod est supprimé brutalement (Crash-Test) ?
**Réponse modèle :** La boucle de contrôle du `ReplicaSet` surveille continuellement l'état du cluster via l'API Server. Lorsqu'un Pod est détruit, le ReplicaSet constate un écart entre l'état désiré (déclaré à 2 ou 4 réplicas) et l'état observé (1 ou 3 réplicas). Il ordonne immédiatement au `kubelet` d'instancier un nouveau conteneur conforme au template pour rétablir l'état désiré en moins de deux secondes.  
*📁 Référence : `kubernetes/04-backend-deployment.yaml`.*

### Q15 : Comment les secrets sont-ils gérés dans votre architecture et comment les sécuriser sur AWS ?
**Réponse modèle :** En local, nous utilisons un objet `Secret` Kubernetes encodé en base64, injecté dans le conteneur sous forme de variables d'environnement. En production sur AWS, nous utiliserions **AWS Secrets Manager** ou **AWS Systems Manager Parameter Store** avec chiffrement par clé AWS KMS, synchronisé dans le cluster via l'External Secrets Operator (ESO) avec rotation automatique des identifiants.  
*📁 Référence : `kubernetes/02-api-secret.yaml` & `docs/aws-comparison.md`.*

### Q16 : En quoi l'étude de cas Wikileaks du cours s'applique-t-elle à ContainerLab ?
**Réponse modèle :** Wikileaks a subi une attaque DDoS géante (>10 Gbps) puis une rupture contractuelle brutale par AWS. Cet incident prouve que la résilience repose sur deux piliers : l'élasticité (pouvoir multiplier instantanément les réplicas face à une charge soudaine via `kubectl scale`) et la portabilité sans vendor lock-in (nos conteneurs standardisés OCI peuvent être redéployés à l'identique sur n'importe quel cloud ou sur site en une commande).  
*📁 Référence : Diapositives Cloud Computing (p. 40-47).*

### Q17 : Comment votre projet serait-il déployé sur AWS en production ?
**Réponse modèle :**
- Le cluster Minikube deviendrait un cluster managé **Amazon EKS** Multi-AZ.
- Le NodePort serait remplacé par un **Application Load Balancer (ALB)** avec terminaison SSL et AWS WAF.
- Les images locales seraient publiées sur **Amazon ECR** avec scan de vulnérabilités.
- La base PostgreSQL conteneurisée serait remplacée par une instance managée **Amazon RDS PostgreSQL** Multi-AZ avec basculement automatique et sauvegardes continues.  
*📁 Référence : `docs/aws-comparison.md`.*

### Q18 : Quel est l'équivalent de votre architecture sous Amazon ECS et AWS Fargate ?
**Réponse modèle :** Dans Amazon ECS, le Pod Kubernetes correspond à une **Task Definition** (qui déclare les images, le CPU et la RAM). Le Deployment correspond à un **ECS Service** (qui maintient le nombre de tâches désiré). En mode **AWS Fargate**, nous n'avons aucune machine virtuelle EC2 à gérer : AWS gère le serveur et le noyau, et facture uniquement les ressources consommées à la seconde par nos conteneurs.  
*📁 Référence : `docs/aws-comparison.md` (Section 5).*

---

## 10. Le grand glossaire en une phrase

| Terme Technique | Définition en une phrase | Localisation dans le Projet |
|---|---|---|
| **Hyperviseur** | Logiciel (Type 1 bare-metal ou Type 2 hosted) qui émule du matériel pour exécuter des machines virtuelles complètes avec leur propre OS invité. | Cours Virtualisation (p. 6-7) |
| **chroot** | Appel système Unix (1979) qui modifie le répertoire racine d'un processus, précurseur de l'isolation du système de fichiers des conteneurs. | Cours Conteneurisation (p. 10) |
| **Control Groups (cgroups)** | Mécanisme du noyau Linux (2006) qui bride et surveille la consommation des ressources physiques (CPU, RAM, disques I/O). | `04-backend-deployment.yaml` |
| **Namespaces** | Fonctionnalité du noyau Linux (2008) qui partitionne les ressources globales pour donner à chaque conteneur sa propre vue isolée (PID, réseau, montages). | Noyau Linux hôte (Docker/K8s) |
| **OverlayFS** | Système de fichiers empilant des couches immuables en lecture seule sous une fine couche supérieure inscriptible en Copy-on-Write (CoW). | Moteur de stockage Docker |
| **Multi-Stage Build** | Technique Dockerfile qui sépare l'étape de compilation logicielle de l'étape d'exécution finale pour minimiser la taille et sécuriser l'image. | `application/frontend/Dockerfile` |
| **Docker Compose** | Outil d'orchestration locale permettant de déclarer et démarrer plusieurs conteneurs interconnectés via un fichier YAML unique. | `compose.yaml` |
| **Zone Démilitarisée (DMZ)** | Sous-réseau intermédiaire isolant les serveurs exposés à Internet des systèmes internes critiques et des bases de données. | `frontend-net` / `backend-net` |
| **Pod** | La plus petite unité déployable et orchestrable dans Kubernetes, regroupant un ou plusieurs conteneurs partageant la même IP et le même stockage. | Objets Pods du cluster |
| **ReplicaSet** | Contrôleur Kubernetes dont l'unique mission est de garantir qu'un nombre précis de réplicas identiques d'un Pod sont en cours d'exécution. | Géré par les Deployments |
| **Deployment** | Objet déclaratif Kubernetes de niveau supérieur qui supervise les ReplicaSets et permet les montées de version (rollout) sans interruption. | `04-backend-deployment.yaml` |
| **Service ClusterIP** | Service Kubernetes interne fournissant une adresse IP virtuelle stable et un nom DNS pour équilibrer le trafic au sein du cluster. | `03-database-service.yaml` |
| **Service NodePort** | Service Kubernetes exposant une application à l'extérieur du cluster via un port statique dédié sur tous les nœuds de calcul. | `05-frontend-service.yaml` |
| **kube-proxy** | Composant réseau exécuté sur chaque nœud Kubernetes qui traduit les IPs virtuelles des Services vers les Pods réels via `iptables`. | Nœud Minikube |
| **kubelet** | Agent principal exécuté sur chaque nœud Kubernetes qui communique avec l'API Server et pilote le runtime de conteneurs pour exécuter les Pods. | Nœud Minikube |
| **etcd** | Base de données clé-valeur distribuée hautement cohérente stockant l'intégralité de l'état et de la configuration du cluster Kubernetes. | Control Plane Kubernetes |
| **ConfigMap** | Objet Kubernetes découplant les paramètres de configuration applicatifs non-confidentiels du code et des images de conteneurs. | `01-api-configmap.yaml` |
| **Secret** | Objet Kubernetes stockant et injectant des données confidentielles (mots de passe, clés d'API) encodées en base64 de façon sécurisée. | `02-api-secret.yaml` |
| **PersistentVolume (PV)** | Ressource physique de stockage de données provisionnée dans le cluster, ayant un cycle de vie indépendant de la vie des Pods. | Provisionné par Minikube HostPath |
| **PersistentVolumeClaim (PVC)** | Requête formelle de stockage émise par une application spécifiant la taille et les modes d'accès requis. | `03-database-pvc.yaml` |
| **StorageClass** | Fournisseur de stockage décrivant les classes et paramètres des volumes alloués dynamiquement dans le cluster. | `standard` (hostpath Minikube) |
| **Liveness Probe** | Sonde Kubernetes vérifiant si le processus applicatif est toujours vivant, déclenchant un redémarrage du conteneur en cas d'échec. | `04-backend-deployment.yaml` |
| **Readiness Probe** | Sonde Kubernetes vérifiant si le conteneur est prêt à recevoir du trafic réseau, le retirant temporairement du Service en cas d'échec. | `04-backend-deployment.yaml` |
| **Horizontal Pod Autoscaler (HPA)** | Contrôleur Kubernetes ajustant automatiquement le nombre de réplicas d'un déploiement en fonction de la charge CPU ou RAM observée. | Métriques cgroups |
| **Algorithme Sandpiper** | Système de gestion automatisée de machines virtuelles détectant les hotspots matériels et orchestrant la migration à chaud de VMs. | Cours Virtualisation (p. 25-28) |
| **IaaS (Infrastructure as a Service)** | Modèle cloud fournissant des ressources matérielles brutes (serveurs, stockage, réseaux) configurées et gérées manuellement. | LAB-01 AWS EC2 |
| **PaaS / CaaS** | Modèle cloud abstrayant le système d'exploitation et l'infrastructure pour délivrer une plateforme d'exécution prête à l'emploi. | ContainerLab / AWS EKS / ECS |
| **Amazon EKS** | Service managé d'orchestration Kubernetes de haute disponibilité délivré par Amazon Web Services. | `docs/aws-comparison.md` |
| **Amazon ECS** | Orchestrateur de conteneurs hautement performant développé spécifiquement par et pour l'écosystème AWS. | `docs/aws-comparison.md` |
| **AWS Fargate** | Moteur de calcul serverless pour Amazon ECS et EKS éliminant totalement la gestion des serveurs physiques et des instances EC2. | `docs/aws-comparison.md` |
| **Application Load Balancer (ALB)** | Équilibreur de charge de niveau 7 (HTTP/HTTPS) géré par AWS avec terminaison SSL et routage avancé par chemins. | Équivalent cloud de NodePort/Nginx |
| **Amazon RDS** | Service de base de données relationnelle managée avec réplication synchrone Multi-AZ et sauvegardes continues automatisées. | Équivalent cloud du conteneur DB |

---

## 11. Checklist avant la soutenance & conseils pour le jour J

### La Veille au Soir (J-1)
- [ ] Dépôt Git propre : vérifiez que `git status` n'affiche aucun fichier non suivi ou en conflit.
- [ ] Exécuter la suite complète de tests de validation : `.\\scripts\\run-tests.ps1` (doit se solder par un sans-faute vert T01 à T11).
- [ ] Batterie de l'ordinateur portable chargée à 100% et chargeur placé dans le sac de cours.
- [ ] Document PDF de soutenance imprimé ou ouvert sur tablette/téléphone pour révision de dernière minute.

### 15 Minutes Avant le Passage
- [ ] Lancer **Docker Desktop** et attendre l'icône verte *"Engine running"*.
- [ ] Démarrer le cluster Minikube : `minikube start --driver=docker`.
- [ ] Précharger les images dans le cluster : `.\\scripts\\load-images.ps1`.
- [ ] Déployer l'application : `.\\scripts\\deploy-k8s.ps1`.
- [ ] Ouvrir une fenêtre PowerShell scindée avec la surveillance des Pods en temps réel :
  ```powershell
  kubectl get pods -n containerlab -w
  ```
- [ ] Ouvrir le navigateur sur l'interface ContainerLab (`http://localhost:3000` ou port-forward `30080`) et vérifier que les 3 voyants sont au vert.
- [ ] Augmenter la taille de police du terminal (Ctrl + Molette) pour garantir une parfaite lisibilité par le jury à 2 mètres de distance.

### Pendant la Soutenance
- [ ] Respecter scrupuleusement la répartition des temps de parole convenue (Houssem : 5 min, Nour : 5 min).
- [ ] Ne parlez jamais les yeux fixés sur vos notes : regardez le jury et commentez les événements visibles sur votre écran.
- [ ] Pour chaque affirmation théorique, montrez la preuve concrète dans le code source ou dans le terminal.
- [ ] Si une question vous est posée pendant la démonstration, répondez calmement en vous appuyant sur la Section 9 de ce guide.

### Après les Questions du Jury
- [ ] Remerciez chaleureusement le jury pour leurs remarques et questions.
- [ ] Nettoyez proprement l'environnement d'évaluation avec la commande :
  ```powershell
  .\\scripts\\cleanup.ps1
  ```
"""

base_dir = os.path.dirname(os.path.abspath(__file__))
md_path = os.path.join(base_dir, "guide-apprentissage-soutenance.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_builder)

print(f"Full markdown guide successfully written! Size: {len(md_builder)} bytes to {md_path}")
