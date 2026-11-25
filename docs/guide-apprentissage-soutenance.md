# ContainerLab — Guide d’Apprentissage, de Démo et de Soutenance
### *Architecture Web Multi-Tiers Résiliente : De Docker Compose à l'Orchestration Kubernetes sur Minikube & Projection Cloud AWS*

| Métadonnée | Information |
| :--- | :--- |
| **Binôme d'étudiants** | Houssem Sassi & Nour El Houde Jaziri |
| **Institution** | ESSTHS (École Supérieure des Sciences et de la Technologie de Hammam Sousse) |
| **Matière** | Virtualisation et Cloud Computing |
| **Enseignantes** | Mme Imen Nasr & Mme Maymouna Ben Said |
| **Sujet** | Proposition 2 — Conteneurisation et Orchestration locale vs Cloud |
| **Année Universitaire** | 2025–2026 |
| **Barème Visé** | 20 / 20 (Rubrique officielle respectée à 100%) |

---

## 1. Comment lire et utiliser ce guide
Ce document est un **manuel d'apprentissage complet et de préparation opérationnelle** à l'épreuve orale et pratique de *Virtualisation & Cloud Computing*. Conçu pour notre binôme (Houssem et Nour), il vous permet de comprendre chaque rouage de **ContainerLab** de l'intérieur, d'établir un lien formel avec chaque notion théorique enseignée par **Mme Imen Nasr** et **Mme Maymouna Ben Said**, et de maîtriser parfaitement la démonstration chronométrée ainsi que les questions pointues du jury.

### Système de repérage visuel (Badges de couleur)
- **[NOTION DU COURS]** : Concept théorique direct issu des diapositives ou LABs des enseignantes (`cgroups`, `namespaces`, `chroot`, `OverlayFS`, `Type-1/2`, `NAT/Bridge`, `IaaS/PaaS/SaaS`).
- **[FAIT ET VÉRIFIÉ]** : Fonctionnalité implémentée, exécutée et validée par notre suite de tests (`7/7 tests unitaires Node.js`, `T01 à T11 validés`, `multi-stage -93.1%`, `self-healing`).
- **[POINT D'ATTENTION]** : Subtilité d'architecture ou décision technique cruciale à justifier (`strategy: Recreate` sur ReadWriteOnce, découplage des sondes Liveness/Readiness, Nginx Reverse Proxy).
- **[BUG & PIÈGE ÉVITÉ]** : Incident technique réel résolu pendant le développement (`Multi-Attach volume error`, crash en cascade de l'API, appel direct du port interne depuis le navigateur).
- **[CLOUD AWS]** : Projection d'architecture cloud d'entreprise (`Amazon EKS`, `Amazon ECS / Fargate`, `ALB`, `RDS Multi-AZ`, `ECR`).

---

## 2. Le projet ContainerLab en 5 minutes
**ContainerLab** est une application web multi-tiers (3-tiers) moderne et résiliente, conçue pour matérialiser la Proposition 2 du cours de Virtualisation & Cloud Computing :
1. **Tier 1 : Frontend & Reverse Proxy** : React 19 SPA servie par `nginx:stable-alpine-slim` sur port 3000 (Compose) ou port 30080 (NodePort K8s).
2. **Tier 2 : Backend API** : Node.js 24 LTS Express API exécutée sous utilisateur non-privilégié (`USER node`), port interne 5000.
3. **Tier 3 : Base de Données** : PostgreSQL 16 Alpine avec schéma `init.sql`, port interne 5432, isolée dans `backend-net`.

### Console d'Observabilité Interactive
- **Live Serving Replica Badge** : Affiche le nom d'hôte exact du Pod traitant la requête (`/api/instance`).
- **Indicateurs de santé** : Statut en direct du Reverse Proxy (80), de l'API (5000) et de la base (5432).
- **Testeur de répartition de charge** : Envoie 6 requêtes en rafale pour observer l'alternance des réplicas pilotés par `kube-proxy`.
- **Fil d'annonces persistantes** : Prouve la conservation des données en base relationnelle lors des crash-tests.

---

## 3. Le pont complet avec le cours des professeures

### 3.1 Virtualisation Matérielle vs Conteneurisation OS
- **Cours :** Hyperviseurs Type 1 (bare-metal) et Type 2 (hosted) émulent du matériel complet avec OS invité (Go, minutes).
- **ContainerLab :** Conteneurs légers partageant le même noyau Linux hôte, démarrage sub-seconde, images de 5.56 à 110 Mo, densité maximale.

### 3.2 Fondations Linux : chroot, cgroups et namespaces
- `chroot` (1979) : isolation du système de fichiers racine (`RootFS`).
- `cgroups` (2006) : gouvernance des ressources physiques. Dans notre manifeste K8s : `requests` (100m CPU / 128Mi RAM) et `limits` (250m CPU / 256Mi RAM).
- `namespaces` (2008) : isolation de la vue des processus. PID (processus vu en PID 1), NET (interfaces `eth0` privées), UTS (hostname du pod), USER (`USER node` non-root), MNT (volumes).

### 3.3 De LXC à Docker
- LXC gérait des conteneurs système multi-processus. Docker applique la philosophie **"un conteneur = un service"**, standardise le Dockerfile et élimine les dépendances avec `libcontainer`.

### 3.4 OverlayFS & Multi-Stage Build
- Couches immuables en lecture seule + couche inscriptible Copy-on-Write (CoW).
- Dans `application/frontend/Dockerfile`, le multi-stage build compile sous Node.js 24 puis ne garde que `dist/` sous Nginx. **Gain mesuré de 93.1% (80.92 MB -> 5.56 MB)** !

### 3.5 Réseaux : Virtualisation vs Conteneurs
- Bridging, NAT, Host-Only du cours.
- Sous Docker Compose : DMZ bi-réseau (`frontend-net` public ↔ `backend-net` privé). Le frontend ne peut techniquement pas pinger PostgreSQL.
- Sous Kubernetes : Services `ClusterIP` (routage interne VIP) et `NodePort` (accès externe sur port 30080).

### 3.6 Stockage et Persistance
- Stockage éphémère vs volumes nommés sous Compose (`postgres_data`).
- Sous Kubernetes : `PersistentVolumeClaim` (PVC) dynamique de 1Gi sur `standard` StorageClass.

### 3.7 Modèles de Service & Déploiement Cloud
- IaaS (EC2 du LAB-01), PaaS (Kubernetes), SaaS (ContainerLab vu par l'utilisateur final).
- Public, Privé, Hybride, Communautaire.
- Cas Wikileaks : DDoS (>10 Gbps), rupture de contrat AWS, résilience par le scaling et absence de vendor lock-in.
- Sandpiper (détection de hotspots de VM et migration live) vs Kubernetes (autoscaling horizontal et réconciliation continue).
- LAB-01 EC2 & LAB-02 VPC : notre segmentation reproduit exactement les sous-réseaux public/privé du LAB-02.

---

## 4. L'architecture expliquée simplement & en vrai code

### Pourquoi Nginx en Reverse Proxy ? (Question n°1 à l'oral)
React s'exécute dans le navigateur de l'hôte (Windows). L'hôte est incapable de résoudre le DNS interne `http://api:5000`. Nginx intercepte `/api/*` et le relaie en interne vers le conteneur API. Bénéfices : Same-Origin (zéro erreur CORS), un seul port public, ports internes hermétiquement protégés.

---

## 5. La démo pas à pas (Scénario chronométré 8 à 10 minutes)
1. **[0:00 - 1:00]** Cadrage académique (Houssem).
2. **[1:00 - 2:30]** Démonstration Docker Compose & Isolation DMZ (Houssem).
3. **[2:30 - 3:30]** Benchmarks des Dockerfiles (-93.1%) (Houssem).
4. **[3:30 - 4:45]** Déploiement déclaratif Kubernetes (10 manifestes) (Nour).
5. **[4:45 - 6:00]** Navigation sur le dashboard & test inter-tiers (Nour).
6. **[6:00 - 7:00]** MOMENT FORT 1 : Scaling 2->4 Pods & répartition de charge `kube-proxy` (Nour).
7. **[7:00 - 8:00]** MOMENT FORT 2 : Crash-Test d'Auto-Guérison (Pod API détruit et recréé en 1.5s) (Houssem).
8. **[8:00 - 9:00]** MOMENT FORT 3 : Crash-Test de Persistance (Pod DB détruit, données intactes via PVC) (Houssem).
9. **[9:00 - 9:45]** Projection Cloud AWS (EKS, ECS Fargate, ALB, RDS Multi-AZ) (Nour).
10. **[9:45 - 10:00]** Conclusion et ouverture aux questions (Binôme).

---

## 6. Les 8 règles d'or d'ingénierie à connaître par cœur
1. Multi-Stage Build obligatoire pour les applications compilées (-93.1%).
2. Stratégie `Recreate` impérative sur PostgreSQL pour éviter l'erreur `Multi-Attach` sur volume `ReadWriteOnce`.
3. Découpler la sonde de vivacité (`/api/health/live`) de la sonde de préparation (`/api/health/ready`) pour prévenir les reboots en cascade.
4. `imagePullPolicy: Never` et tags sémantiques stricts pour l'évaluation locale hors-ligne.
5. Exécution non-root (`USER node`) pour le principe de moindre privilège.
6. Le Namespace est une frontière administrative, pas un pare-feu réseau.
7. `condition: service_healthy` dans Docker Compose pour un ordonnancement déterministe.
8. Service NodePort 30080 pour l'indépendance vis-à-vis des contrôleurs cloud.

---

## 7. La suite de tests automatisée (Unitaires + T01 à T11)
- 7 tests unitaires Node.js (`test/api.test.js`) réussis avec code 0.
- Matrice T01 à T11 validée : Build, Benchmark, Compose, CRUD, Restart, K8s Rollout, Traffic distribution, Scaling 2->4, Self-healing, PVC persistence, Cleanup.

---

## 8. Les bugs réels rencontrés et leçons apprises
- Résolution du `Multi-Attach error` via `strategy: Recreate`.
- Résolution de `ERR_NAME_NOT_RESOLVED` via reverse proxy Nginx.
- Résolution de `ImagePullBackOff` via `imagePullPolicy: Never`.
- Résolution des reboots en cascade via sondes découplées.

---

## 9. Questions probables à la soutenance (18 Q&R d'experts)
*(Voir document complet pour les 18 réponses modèles détaillées et fichiers sources associés)*.

---

## 10. Le grand glossaire en une phrase (32 termes clés)

---

## 11. Checklist avant la soutenance
- La veille au soir : git propre, tests verts, chargeur.
- 15 minutes avant : Docker Desktop, Minikube lancé, dashboard ouvert.
- Pendant l'oral : alternance de parole, montrer le code et les terminaux.
