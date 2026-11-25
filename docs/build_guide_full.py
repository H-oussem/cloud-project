# -*- coding: utf-8 -*-
"""
Full Generator for ContainerLab Learning, Demo & Defense Guide
Generates comprehensive Markdown, standalone styled HTML with Base64 screenshots,
and compiles the final PDF directly onto the user's Desktop.
"""

import os
import sys
import base64
import subprocess

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    return ""

def main():
    base_dir = r"c:\Users\houss\Desktop\Cloud project"
    screenshots_dir = os.path.join(base_dir, "docs", "screenshots")
    
    img_dashboard = get_base64_image(os.path.join(screenshots_dir, "dashboard.png"))
    img_compose = get_base64_image(os.path.join(screenshots_dir, "docker-compose-status.png"))
    img_k8s = get_base64_image(os.path.join(screenshots_dir, "kubernetes-status.png"))
    
    print("Screenshots encoded in Base64.")
    
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        @page {
            size: A4 portrait;
            margin: 14mm 12mm 14mm 12mm;
            @bottom-right {
                content: counter(page);
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 8pt;
                color: #64748b;
            }
        }

        *, *:before, *:after {
            box-sizing: border-box;
        }

        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            color: #0f172a;
            background-color: #ffffff;
            font-size: 9.8pt;
            line-height: 1.55;
            margin: 0;
            padding: 0;
        }

        h1, h2, h3, h4, h5 {
            color: #0f172a;
            font-weight: 700;
            margin-top: 1.4em;
            margin-bottom: 0.5em;
            line-height: 1.25;
            page-break-after: avoid;
            break-after: avoid;
        }

        h1 {
            font-size: 22pt;
            color: #1e3a8a;
            border-bottom: 2.5px solid #2563eb;
            padding-bottom: 8px;
            margin-top: 0;
        }

        h2 {
            font-size: 14.5pt;
            color: #1e40af;
            border-bottom: 1.5px solid #e2e8f0;
            padding-bottom: 5px;
            margin-top: 1.6em;
        }

        h3 {
            font-size: 11.5pt;
            color: #0369a1;
            margin-top: 1.2em;
        }

        h4 {
            font-size: 10.2pt;
            color: #334155;
            margin-top: 1em;
        }

        p {
            margin-top: 0;
            margin-bottom: 0.8em;
            text-align: justify;
        }

        a {
            color: #2563eb;
            text-decoration: none;
            font-weight: 500;
        }

        .badge {
            display: inline-block;
            padding: 2px 7px;
            font-size: 7.5pt;
            font-weight: 700;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            margin-right: 4px;
            vertical-align: middle;
        }
        .badge-blue { background-color: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }
        .badge-green { background-color: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
        .badge-yellow { background-color: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
        .badge-red { background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
        .badge-purple { background-color: #f3e8ff; color: #6b21a8; border: 1px solid #e9d5ff; }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0 16px 0;
            font-size: 8.8pt;
            page-break-inside: auto;
        }

        thead {
            display: table-header-group;
        }

        tr {
            page-break-inside: avoid;
            page-break-after: auto;
        }

        th, td {
            padding: 7px 9px;
            text-align: left;
            vertical-align: top;
            border: 1px solid #cbd5e1;
        }

        th {
            background-color: #f8fafc;
            color: #1e293b;
            font-weight: 700;
            font-size: 8.5pt;
        }

        tr:nth-child(even) td {
            background-color: #fcfdfe;
        }

        .callout {
            padding: 9px 13px;
            margin: 10px 0 14px 0;
            border-radius: 5px;
            border-left: 4px solid;
            font-size: 9.2pt;
            page-break-inside: avoid;
        }

        .callout-info {
            background-color: #eff6ff;
            border-left-color: #3b82f6;
            color: #1e3a8a;
        }

        .callout-success {
            background-color: #f0fdf4;
            border-left-color: #22c55e;
            color: #14532d;
        }

        .callout-warning {
            background-color: #fffbeb;
            border-left-color: #f59e0b;
            color: #78350f;
        }

        .callout-danger {
            background-color: #fef2f2;
            border-left-color: #ef4444;
            color: #7f1d1d;
        }

        .callout-purple {
            background-color: #faf5ff;
            border-left-color: #a855f7;
            color: #581c87;
        }

        .callout-title {
            font-weight: 700;
            margin-bottom: 3px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        pre {
            background-color: #0f172a;
            color: #e2e8f0;
            padding: 9px 12px;
            border-radius: 5px;
            font-family: 'JetBrains Mono', 'Cascadia Code', Consolas, monospace;
            font-size: 8pt;
            line-height: 1.45;
            overflow-x: auto;
            margin: 8px 0 12px 0;
            page-break-inside: avoid;
            border: 1px solid #1e293b;
        }

        code {
            font-family: 'JetBrains Mono', 'Cascadia Code', Consolas, monospace;
            font-size: 8.5pt;
            background-color: #f1f5f9;
            color: #0f172a;
            padding: 1px 4px;
            border-radius: 3px;
            border: 1px solid #e2e8f0;
        }

        pre code {
            background-color: transparent;
            color: inherit;
            padding: 0;
            border: none;
            font-size: 8pt;
        }

        .cover-box {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
            color: #ffffff;
            padding: 22px 24px;
            border-radius: 8px;
            margin-bottom: 18px;
        }

        .cover-title {
            font-size: 20pt;
            font-weight: 800;
            margin: 0 0 6px 0;
            color: #ffffff;
            letter-spacing: -0.5px;
        }

        .cover-subtitle {
            font-size: 11pt;
            color: #93c5fd;
            margin: 0 0 14px 0;
            font-weight: 400;
            line-height: 1.4;
        }

        .meta-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px 18px;
            font-size: 8.5pt;
            background: rgba(255, 255, 255, 0.08);
            padding: 12px 14px;
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        .meta-item strong {
            color: #bfdbfe;
        }

        .screenshot-container {
            margin: 12px 0 16px 0;
            text-align: center;
            page-break-inside: avoid;
        }

        .screenshot-img {
            max-width: 95%;
            max-height: 275px;
            object-fit: contain;
            border-radius: 6px;
            border: 1px solid #cbd5e1;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        }

        .screenshot-caption {
            font-size: 8pt;
            color: #64748b;
            margin-top: 4px;
            font-style: italic;
        }

        .qa-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            margin-bottom: 12px;
            page-break-inside: avoid;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }

        .qa-header {
            background-color: #f8fafc;
            padding: 7px 11px;
            border-bottom: 1px solid #e2e8f0;
            font-weight: 700;
            color: #1e3a8a;
            font-size: 9.2pt;
        }

        .qa-body {
            padding: 9px 12px;
            font-size: 9pt;
        }

        .qa-body p:last-child {
            margin-bottom: 0;
        }

        .qa-cite {
            display: inline-block;
            margin-top: 5px;
            font-size: 8pt;
            color: #0284c7;
            font-weight: 600;
        }

        .step-box {
            border-left: 3px solid #2563eb;
            background-color: #f8fafc;
            padding: 8px 12px;
            margin-bottom: 10px;
            border-radius: 0 6px 6px 0;
            page-break-inside: avoid;
        }

        .step-header {
            font-weight: 700;
            color: #1e40af;
            font-size: 9.3pt;
            display: flex;
            justify-content: space-between;
            margin-bottom: 4px;
        }

        .page-break {
            page-break-before: always;
        }

        ul, ol {
            margin-top: 0;
            margin-bottom: 0.8em;
            padding-left: 20px;
        }

        li {
            margin-bottom: 0.3em;
        }

        .diagram-box {
            background-color: #f8fafc;
            border: 1px solid #cbd5e1;
            padding: 10px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 7.8pt;
            line-height: 1.35;
            white-space: pre;
            overflow-x: auto;
            margin: 10px 0;
            color: #1e293b;
            page-break-inside: avoid;
        }
    </style>
    """
    
    # Assemble HTML
    html_parts = []
    html_parts.append("<!DOCTYPE html><html lang='fr'><head><meta charset='UTF-8'><title>ContainerLab — Guide d’apprentissage, de démo et de soutenance</title>")
    html_parts.append(css)
    html_parts.append("</head><body>")
    
    # COVER BOX
    html_parts.append("""
    <div class="cover-box">
        <div class="cover-title">ContainerLab — Guide d’Apprentissage, de Démo et de Soutenance</div>
        <div class="cover-subtitle">Architecture Web Multi-Tiers Résiliente : De Docker Compose à l'Orchestration Kubernetes sur Minikube & Projection Cloud AWS</div>
        <div class="meta-grid">
            <div class="meta-item"><strong>Étudiants :</strong> Houssem Sassi & Nour El Houde Jaziri</div>
            <div class="meta-item"><strong>Institution :</strong> ESSTHS (École Supérieure des Sciences et de la Technologie de Hammam Sousse)</div>
            <div class="meta-item"><strong>Matière :</strong> Virtualisation et Cloud Computing</div>
            <div class="meta-item"><strong>Enseignantes :</strong> Mme Imen Nasr & Mme Maymouna Ben Said</div>
            <div class="meta-item"><strong>Sujet :</strong> Proposition 2 — Conteneurisation et Orchestration locale vs Cloud</div>
            <div class="meta-item"><strong>Barème Visé :</strong> 20 / 20 (Rubrique officielle respectée à 100%)</div>
        </div>
    </div>
    """)
    
    # SECTION 1
    html_parts.append("""
    <h2>1. Comment lire et utiliser ce guide</h2>
    <p>Ce document est un <strong>manuel d'apprentissage complet et de préparation opérationnelle</strong> à l'épreuve orale et pratique de <em>Virtualisation & Cloud Computing</em>. Conçu pour notre binôme (Houssem et Nour), il vous permet de comprendre chaque rouage de <strong>ContainerLab</strong> de l'intérieur, d'établir un lien formel avec chaque notion théorique enseignée par <strong>Mme Imen Nasr</strong> et <strong>Mme Maymouna Ben Said</strong>, et de maîtriser parfaitement la démonstration chronométrée ainsi que les questions pointues du jury.</p>

    <div class="callout callout-info">
        <div class="callout-title">💡 Méthode d'entraînement pour la soutenance</div>
        Pour chaque section et chaque question de soutenance, <strong>tentez de répondre à voix haute</strong> avant de lire la réponse modèle. Entraînez-vous à alterner la parole avec fluidité et sachez exactement quel fichier ouvrir dans VS Code pour prouver techniquement vos propos.
    </div>

    <p>Le document utilise un code couleur standardisé sous forme de badges pour identifier instantanément la portée de chaque information :</p>
    <table>
        <thead>
            <tr>
                <th style="width: 18%;">Badge & Couleur</th>
                <th style="width: 32%;">Signification Pédagogique</th>
                <th style="width: 50%;">Exemple Concret dans ContainerLab</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><span class="badge badge-blue">Notion du cours</span></td>
                <td>Concept théorique direct issu des diapositives ou LABs des enseignantes.</td>
                <td><code>cgroups</code>, <code>namespaces</code> (PID/NET/MNT), <code>chroot</code>, <code>OverlayFS</code>, <code>Type-1/2</code>, <code>NAT/Bridge</code>, <code>IaaS/PaaS/SaaS</code>.</td>
            </tr>
            <tr>
                <td><span class="badge badge-green">Fait & Vérifié</span></td>
                <td>Fonctionnalité implémentée, exécutée et validée par notre suite de tests.</td>
                <td><code>7/7 tests unitaires Node.js</code>, <code>T01 à T11 validés</code>, <code>multi-stage -93.1%</code>, <code>self-healing</code>.</td>
            </tr>
            <tr>
                <td><span class="badge badge-yellow">Point d'attention</span></td>
                <td>Subtilité d'architecture ou décision technique cruciale à justifier.</td>
                <td><code>strategy: Recreate</code> (ReadWriteOnce), découplage des sondes Liveness/Readiness, Nginx Reverse Proxy.</td>
            </tr>
            <tr>
                <td><span class="badge badge-red">Bug & Piège évité</span></td>
                <td>Incident technique réel résolu pendant le développement ou piège classique d'examen.</td>
                <td><code>Multi-Attach volume error</code>, crash en cascade de l'API, appel direct du port interne depuis le navigateur.</td>
            </tr>
            <tr>
                <td><span class="badge badge-purple">Cloud AWS</span></td>
                <td>Projection d'architecture cloud d'entreprise au-delà de l'environnement local.</td>
                <td>Équivalents de production : <code>Amazon EKS</code>, <code>Amazon ECS / Fargate</code>, <code>ALB</code>, <code>RDS Multi-AZ</code>, <code>ECR</code>.</td>
            </tr>
        </tbody>
    </table>
    """)
    
    # SECTION 2
    html_parts.append("""
    <h2>2. Le projet ContainerLab en 5 minutes</h2>
    <p><strong>ContainerLab</strong> est une implémentation académique d'excellence d'une application web multi-tiers (3-tiers) résiliente, conçue pour répondre à l'intégralité du cahier des charges de la <strong>Proposition 2 : Conteneurisation et Orchestration locale vs Cloud (Docker & Kubernetes / ECS)</strong>.</p>
    
    <p>Le projet matérialise le passage de la <em>virtualisation lourde</em> par hyperviseur (qui clone un OS invité complet avec son noyau) vers la <em>conteneurisation légère</em> (qui isole des processus partageant le même noyau Linux), à travers deux stades d'orchestration complémentaires :</p>
    
    <ol>
        <li><strong>Stade 1 : Composition locale avec Docker Compose</strong> : segmentation réseau en zone démilitarisée (DMZ), synchronisation déterministe au démarrage via des sondes d'état saines (<code>condition: service_healthy</code>), et persistance des données sur volume nommé Docker.</li>
        <li><strong>Stade 2 : Orchestration de Cluster avec Kubernetes sur Minikube</strong> : déploiement déclaratif de 10 manifestes ordonnés dans un Namespace isolé, provisionnement dynamique de stockage persistant (PVC 1Gi), découplage fin des sondes de vie et de préparation, équilibrage de charge via <code>kube-proxy</code>, redimensionnement dynamique de 2 à 4 réplicas, et auto-guérison autonome en cas de crash de conteneur.</li>
    </ol>

    <h3>Les 3 Tiers de l'Architecture Applicative</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 20%;">Composant (Tier)</th>
                <th style="width: 25%;">Technologies & Images</th>
                <th style="width: 25%;">Rôle & Fonctionnalités</th>
                <th style="width: 30%;">Sécurité & Réseau</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Tier 1 : Frontend & Reverse Proxy</strong></td>
                <td>React 19 Single Page Application (Vite 6) servie par <code>nginx:stable-alpine-slim</code></td>
                <td>Délivre l'interface utilisateur, affiche l'observabilité du cluster, et relaie les requêtes <code>/api/*</code> vers le backend.</td>
                <td>Exposé sur <strong>Port 3000</strong> (Compose) ou <strong>Port 30080</strong> (NodePort K8s). Seul point d'entrée externe du système.</td>
            </tr>
            <tr>
                <td><strong>Tier 2 : Backend API</strong></td>
                <td>Node.js 24 LTS + Express REST API</td>
                <td>Exécute la logique métier, la validation stricte des entrées, les sondes de santé, et interroge la base PostgreSQL.</td>
                <td>Exécution non-root (<code>USER node</code>). Port interne <strong>5000</strong>. Invisible depuis l'extérieur du réseau de conteneurs.</td>
            </tr>
            <tr>
                <td><strong>Tier 3 : Base de Données</strong></td>
                <td>PostgreSQL 16 Alpine avec script d'initialisation <code>init.sql</code></td>
                <td>Assure le stockage persistant et relationnel des annonces et métadonnées système.</td>
                <td>Port interne <strong>5432</strong>. Isolée dans la DMZ <code>backend-net</code> (inaccessible au Frontend sous Docker Compose).</td>
            </tr>
        </tbody>
    </table>

    <h3>La Console d'Observabilité Interactive Intégrée</h3>
    <p>Pour rendre la soutenance dynamique et immédiatement convaincante, le Frontend intègre un tableau de bord d'observabilité réactif conçu sur mesure :</p>
    <ul>
        <li><strong>Badge de Réplica Actif (Live Serving Replica)</strong> : Interroge <code>GET /api/instance</code> pour afficher le nom d'hôte exact du conteneur ou Pod traitant la requête (ex: <code>api-7d498b58f9-k2x89</code>), avec un bouton de copie rapide pour le crash-test.</li>
        <li><strong>Indicateurs de Santé Temps Réel (Three-Tier Health Status)</strong> : Feux tricolores surveillant le serveur web Nginx (:80), la vivacité de l'API (:5000) et la connectivité active au pool PostgreSQL (:5432).</li>
        <li><strong>Testeur de Répartition de Charge (Traffic Distribution)</strong> : Un bouton envoie une rafale de 6 requêtes asynchrones en parallèle. L'interface affiche l'alternance des noms de Pods retournés, prouvant le load-balancing opéré par <code>kube-proxy</code>.</li>
        <li><strong>Fil d'Annonces Persistantes</strong> : Permet de créer, valider et lister des annonces stockées en base relationnelle, servant de témoin infaillible pour les tests de persistance lors des redémarrages.</li>
    </ul>

    <div class="screenshot-container">
        <img class="screenshot-img" src='""" + img_dashboard + """' alt='Dashboard ContainerLab' />
        <div class="screenshot-caption">Figure 1 : Interface d'observabilité de ContainerLab affichant le statut sain des 3 tiers, le nom du Pod actif et le fil d'annonces persistantes.</div>
    </div>
    """)
    
    # SECTION 3
    html_parts.append("""
    <div class="page-break"></div>
    <h2>3. Le pont complet avec le cours des professeures</h2>
    <p>Cette section est la clé de voûte de votre préparation : elle établit une <strong>passerelle directe et systématique</strong> entre les notions enseignées en cours magistral par <strong>Mme Imen Nasr</strong> et <strong>Mme Maymouna Ben Said</strong> et leur réalisation concrète dans ContainerLab.</p>

    <h3>3.1 Virtualisation Matérielle vs Conteneurisation OS</h3>
    <p><span class="badge badge-blue">Cours Conteneurisation (slides 4 à 7)</span> <span class="badge badge-blue">Cours Virtualisation (slides 4 à 7)</span></p>
    <ul>
        <li><strong>Ce que le cours enseigne :</strong> La virtualisation matérielle classique s'appuie sur un <em>Hyperviseur</em> (Type 1 bare-metal comme VMware ESXi/Hyper-V ou Type 2 hosted comme VirtualBox/VMware Workstation) pour émuler une machine physique complète. Chaque VM embarque son propre système d'exploitation invité (Guest OS), ce qui entraîne une consommation de stockage importante (plusieurs Go), une utilisation mémoire redondante et des temps de démarrage de plusieurs minutes. À l'inverse, la conteneurisation est une <em>virtualisation au niveau du système d'exploitation</em> qui ne virtualise pas le matériel mais crée des environnements isolés pour les processus en s'appuyant directement sur les fonctionnalités du noyau de l'hôte.</li>
        <li><strong>Ce que nous avons fait dans ContainerLab :</strong> Nous avons éliminé toute émulation matérielle. Nos conteneurs (Frontend, API, Database) s'exécutent directement sur le noyau Linux de l'hôte (via Docker Engine / WSL2). Leurs images pèsent entre 5.56 Mo et 110 Mo, démarrent en moins de 2 secondes, et partagent efficacement le CPU et la RAM de l'hôte sans couche d'hyperviseur intermédiaire.</li>
    </ul>

    <h3>3.2 Les Fondations du Noyau Linux : chroot, cgroups et namespaces</h3>
    <p><span class="badge badge-blue">Cours Conteneurisation (slides 10 à 13)</span> <span class="badge badge-blue">Cours Virtualisation (slides 30 à 33)</span></p>
    <p>Le cours explique que la conteneurisation repose historiquement sur trois briques fondamentales du noyau Linux. Voici comment chacune d'elles opère concrètement dans notre projet :</p>
    <table>
        <thead>
            <tr>
                <th style="width: 15%;">Primitive Linux</th>
                <th style="width: 35%;">Définition & Rôle dans le Cours</th>
                <th style="width: 50%;">Mise en Œuvre dans ContainerLab</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>chroot</strong> (1979)</td>
                <td>Commande permettant de changer le répertoire racine (<code>/</code>) d'un processus et de ses sous-processus. Fournit un espace disque isolé ("chroot jail") mais n'offre aucune isolation de processus, de mémoire ou de réseau.</td>
                <td>Chaque conteneur de ContainerLab dispose de son propre système de fichiers racine (<code>RootFS</code>) étanche, empêchant un attaquant éventuel dans l'API d'accéder aux fichiers de l'hôte ou de la base.</td>
            </tr>
            <tr>
                <td><strong>cgroups</strong> (2006)</td>
                <td>Fonctionnalité du noyau Linux pour <em>limiter, compter et isoler l'utilisation des ressources</em> physiques : temps CPU, mémoire vive, bande passante réseau et entrées/sorties disque (I/O).</td>
                <td>Dans notre manifeste <code>06-api-deployment.yaml</code>, nous déclarons des limites strictes :<br><code>resources.requests: { cpu: "100m", memory: "128Mi" }</code><br><code>resources.limits: { cpu: "250m", memory: "256Mi" }</code>.<br>Le noyau Linux bride le CPU et déclenche l'OOM-Killer si la mémoire dépasse 256 MiB, protégeant le cluster du syndrome du "mauvais voisin".</td>
            </tr>
            <tr>
                <td><strong>namespaces</strong> (2008)</td>
                <td>Mécanisme qui partitionne les ressources globales du système pour donner à chaque groupe de processus sa propre vue unique et isolée :
                <ul>
                    <li><code>pid</code> : numérotation des processus</li>
                    <li><code>net</code> : interfaces et tables de routage</li>
                    <li><code>mnt</code> : points de montage de disques</li>
                    <li><code>ipc</code> : mémoire partagée inter-processus</li>
                    <li><code>uts</code> : nom d'hôte (hostname)</li>
                    <li><code>user</code> : mappage des identifiants UID/GID</li>
                </ul></td>
                <td>Dans ContainerLab :
                <ul>
                    <li><strong>PID namespace :</strong> Le serveur Node.js voit son processus comme le PID 1 dans le conteneur API.</li>
                    <li><strong>NET namespace :</strong> Chaque conteneur possède sa propre interface <code>eth0</code> avec son adresse IP privée dédiée.</li>
                    <li><strong>UTS namespace :</strong> Chaque réplica API possède son propre nom d'hôte généré par Kubernetes (ex: <code>api-7d498b58f9-k2x89</code>), affiché sur le dashboard.</li>
                    <li><strong>USER namespace :</strong> L'API s'exécute sous le compte non-privilégié <code>USER node</code> (UID 1000) au lieu de <code>root</code>.</li>
                </ul></td>
            </tr>
        </tbody>
    </table>

    <h3>3.3 De LXC à Docker & la Philosophie "Un Conteneur = Un Service"</h3>
    <p><span class="badge badge-blue">Cours Conteneurisation (slides 16 à 19)</span></p>
    <ul>
        <li><strong>Ce que le cours enseigne :</strong> LXC (2008) a intégré les cgroups et namespaces dans le noyau 2.6.24 pour créer des "conteneurs Linux". Cependant, LXC gère des conteneurs comme de petites machines virtuelles contenant de multiples processus et services. Docker (2013) a révolutionné l'industrie en apportant :
            <ol>
                <li>La philosophie <strong>"un conteneur = un service"</strong> (une application multi-services se décompose en X conteneurs spécialisés).</li>
                <li>Le remplacement de LXC par <code>libcontainer</code> (puis <code>runc</code>) pour communiquer directement avec les APIs du noyau.</li>
                <li>L'automatisation de la construction via le fichier <strong>Dockerfile</strong>.</li>
                <li>La standardisation de la distribution via le concept d'<strong>Image</strong> et les dépôts (Docker Hub / Registries).</li>
            </ol>
        </li>
        <li><strong>Ce que nous avons fait dans ContainerLab :</strong> Notre projet applique fidèlement la règle <em>un conteneur = un service</em> : nous avons créé 3 conteneurs distincts avec leurs propres Dockerfiles (Frontend Nginx, Backend Node.js, Base PostgreSQL), totalement découplés, faciles à maintenir, à mettre à l'échelle individuellement et à remplacer sans interrompre les autres briques.</li>
    </ul>

    <h3>3.4 Système de Fichiers Union (OverlayFS) et Multi-Stage Build</h3>
    <p><span class="badge badge-blue">Cours Conteneurisation (slides 23, 26, 27)</span></p>
    <ul>
        <li><strong>Ce que le cours enseigne :</strong> Une image Docker est une succession de couches immuables (read-only layers) construites instruction par instruction dans le Dockerfile. Lorsqu'un conteneur démarre, Docker ajoute une fine couche inscriptible éphémère (writable layer) via le principe de Copy-on-Write (CoW). Pour optimiser la taille des images et la sécurité, il est crucial d'éliminer les outils de compilation de l'image finale.</li>
        <li><strong>Ce que nous avons fait dans ContainerLab :</strong> Dans <code>application/frontend/Dockerfile</code>, nous avons implémenté un <strong>Multi-Stage Build</strong> rigoureux :
            <ul>
                <li><strong>Étape 1 (builder) :</strong> Utilise <code>node:24-alpine</code> pour télécharger les packages npm et compiler le code React/JSX avec Vite via <code>npm run build</code>.</li>
                <li><strong>Étape 2 (runner) :</strong> Utilise <code>nginx:stable-alpine-slim</code>. Nous copions uniquement le dossier compilé <code>dist/</code> vers <code>/usr/share/nginx/html</code> et notre configuration <code>nginx.conf</code>.</li>
            </ul>
        </li>
    </ul>

    <div class="callout callout-success">
        <div class="callout-title">🏆 Benchmark validé (Test T02) : Réduction de 93.1% de la taille d'image !</div>
        L'image non-optimisée embarquant le runtime Node.js et les outils de développement pesait <strong>80.92 MB</strong>. L'image de production multi-stage ne pèse que <strong>5.56 MB</strong>, soit un gain mesuré de <strong>-93.1%</strong> (-75.36 Mo d'économisés !).
    </div>

    <h3>3.5 Réseaux de Virtualisation vs Réseaux de Conteneurisation</h3>
    <p><span class="badge badge-blue">Cours Virtualisation (slides 25 à 27)</span> <span class="badge badge-blue">Cours Conteneurisation (slides 30 à 32)</span></p>
    <p>Le cours de virtualisation détaille les trois modes d'accès réseau pour les machines virtuelles, et le cours de conteneurisation présente les pilotes Docker. Voici la comparaison directe :</p>
    <table>
        <thead>
            <tr>
                <th style="width: 20%;">Mode Réseau (Cours)</th>
                <th style="width: 40%;">Principe & Fonctionnement</th>
                <th style="width: 40%;">Équivalent Concret dans ContainerLab</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Network Bridging (Pont)</strong></td>
                <td>La VM dispose d'un accès direct au réseau physique indépendamment du système hôte, avec sa propre adresse IP sur le LAN. Dans Docker, le pilote <code>bridge</code> crée un commutateur virtuel logiciel (ex: <code>docker0</code>) isolant les conteneurs sur un sous-réseau privé.</td>
                <td>Sous <strong>Docker Compose</strong>, nous avons créé deux réseaux ponts : <code>frontend-net</code> et <code>backend-net</code>. Les conteneurs communiquent par DNS interne (ex: <code>http://api:5000</code>).</td>
            </tr>
            <tr>
                <td><strong>NAT (Network Address Translation)</strong></td>
                <td>La VM est sur un réseau virtuel privé masqué derrière l'adresse IP de l'hôte. L'hyperviseur effectue une translation d'adresses et de ports (Port Forwarding / Port Publishing <code>-p</code>).</td>
                <td>Le mapping <code>ports: ["3000:80"]</code> dans Compose et <code>nodePort: 30080</code> dans Kubernetes acheminent le trafic de l'hôte vers le port interne du conteneur Nginx.</td>
            </tr>
            <tr>
                <td><strong>Host-Only Networking</strong></td>
                <td>Réseau totalement privé et isolé permettant uniquement la communication entre les VMs et l'hôte, sans aucun accès au monde extérieur.</td>
                <td>Le réseau <code>backend-net</code> de Compose isole la base PostgreSQL. Elle n'expose aucun port sur l'hôte et n'est accessible que par le conteneur API.</td>
            </tr>
            <tr>
                <td><strong>Kubernetes Services (ClusterIP & NodePort)</strong></td>
                <td>Abstractions Kubernetes gérant l'équilibrage de charge et la découverte de services via des adresses IP virtuelles stables et des règles iptables pilotées par <code>kube-proxy</code>.</td>
                <td><code>service/api</code> et <code>service/postgres</code> utilisent <strong>ClusterIP</strong> (VIP interne). <code>service/frontend</code> utilise <strong>NodePort</strong> (port statique 30080).</td>
            </tr>
        </tbody>
    </table>

    <h3>3.6 Stockage et Persistance des Données</h3>
    <p><span class="badge badge-blue">Cours Conteneurisation (slide 34)</span></p>
    <ul>
        <li><strong>Ce que le cours enseigne :</strong> Les conteneurs sont intrinsèquement éphémères : les fichiers modifiés dans la couche inscriptible sont perdus lors de la destruction du conteneur. Le cours présente 3 mécanismes de stockage :
            <ol>
                <li><code>tmpfs mount</code> : stockage volatile en mémoire RAM de l'hôte.</li>
                <li><code>bind mount</code> : montage direct d'un dossier du système de fichiers hôte dans le conteneur.</li>
                <li><code>volume Docker</code> : stockage persistant géré par le moteur Docker, isolé du système de fichiers hôte.</li>
            </ol>
        </li>
        <li><strong>Ce que nous avons fait dans ContainerLab :</strong>
            <ul>
                <li><strong>Sous Docker Compose :</strong> Utilisation d'un volume nommé <code>postgres_data</code> monté sur <code>/var/lib/postgresql/data</code>. Les annonces saisies résistent à la commande <code>docker compose restart postgres</code>.</li>
                <li><strong>Sous Kubernetes :</strong> Déclaration d'un <code>PersistentVolumeClaim</code> (PVC) de 1Gi (<code>03-database-pvc.yaml</code>) provisionné dynamiquement par la <code>standard</code> StorageClass de Minikube. Même si le Pod PostgreSQL est supprimé par <code>kubectl delete pod</code>, le contrôleur recrée un Pod qui s'accroche au même volume persistant, conservant 100% des données (validé par le test T10).</li>
            </ul>
        </li>
    </ul>

    <h3>3.7 Modèles de Service Cloud : IaaS, PaaS, SaaS, NaaS, IDaaS, SSO</h3>
    <p><span class="badge badge-blue">Cours Cloud Computing (slides 15, 16, 50 à 70)</span></p>
    <p>Le cours de Mme Nasr définit les modèles de service de référence ("XaaS - Anything as a Service") ainsi que le partage de responsabilités. Voici comment ContainerLab s'inscrit dans cette taxonomie :</p>
    <table>
        <thead>
            <tr>
                <th style="width: 18%;">Modèle Cloud</th>
                <th style="width: 42%;">Définition du Cours</th>
                <th style="width: 40%;">Positionnement vis-à-vis de ContainerLab</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>IaaS</strong> (Infrastructure as a Service)</td>
                <td>Fournit des ressources fondamentales : machines virtuelles (ex: AWS EC2), stockage en bloc/objet (EBS, S3), et réseau virtuel (VPC). Le client gère l'OS, les runtimes et les applications.</td>
                <td>Nos conteneurs peuvent tourner sur des instances virtuelles IaaS EC2 provisionnées manuellement ou gérées dans un cluster Minikube local.</td>
            </tr>
            <tr>
                <td><strong>PaaS</strong> (Platform as a Service)</td>
                <td>Fournit l'environnement d'exécution, les bibliothèques et les outils de déploiement (ex: AWS Elastic Beanstalk, Heroku). L'utilisateur n'administre pas le serveur ni l'OS.</td>
                <td>Kubernetes fonctionne comme un métamodèle PaaS : il abstrait les machines physiques pour offrir une plateforme d'exécution déclarative.</td>
            </tr>
            <tr>
                <td><strong>SaaS</strong> (Software as a Service)</td>
                <td>L'application logicielle complète est délivrée clé en main via un navigateur web (ex: Gmail, Salesforce, Google Docs). Tout est géré par le fournisseur.</td>
                <td>Du point de vue des utilisateurs finaux qui consultent et postent des annonces dans le navigateur, <strong>ContainerLab fonctionne comme un service SaaS</strong>.</td>
            </tr>
            <tr>
                <td><strong>NaaS</strong> (Network as a Service)</td>
                <td>Virtualisation de l'infrastructure réseau (SDN), déploiement de protocoles de routage personnalisés et connectivité sécurisée à la demande.</td>
                <td>Illustré par notre segmentation en sous-réseaux isolés, répliquée sur AWS via <strong>Amazon VPC</strong>.</td>
            </tr>
            <tr>
                <td><strong>IDaaS & SSO</strong> (Single Sign-On)</td>
                <td>Gestion centralisée des identités et authentification unique basée sur des serveurs de tickets pour éviter les multiples identifiants (cours p. 66-68).</td>
                <td>Dans une extension de production, ContainerLab déléguerait l'authentification à un fournisseur IDaaS (ex: AWS Cognito, Keycloak, Auth0) avec jetons JWT signés.</td>
            </tr>
        </tbody>
    </table>

    <h3>3.8 Modèles de Déploiement Cloud</h3>
    <p><span class="badge badge-blue">Cours Cloud Computing (slides 14, 29 à 39)</span></p>
    <ul>
        <li><strong>Cloud Public :</strong> Infrastructure mutualisée accessible à grande échelle via Internet (AWS, Azure, GCP). Offre une très haute élasticité mais une sécurité partagée. C'est la cible de déploiement cloud de ContainerLab via AWS EKS ou ECS.</li>
        <li><strong>Cloud Privé :</strong> Infrastructure dédiée à une seule organisation. Sécurité et contrôle maximaux, mais coûts d'acquisition de matériel élevés et passage à l'échelle limité. C'est l'équivalent de notre cluster local Minikube sur machine dédiée.</li>
        <li><strong>Cloud Hybride :</strong> Combinaison de cloud privé (pour les données critiques, comme notre base PostgreSQL) et de cloud public (pour absorber les pics de charge sur l'API ou le frontend web).</li>
        <li><strong>Cloud Communautaire :</strong> Infrastructure mutualisée entre plusieurs organisations partageant des exigences communes (ex: plateforme inter-universitaire tunisienne pour les établissements de l'enseignement supérieur).</li>
    </ul>

    <h3>3.9 L'Étude de Cas Wikileaks & Les Leçons de Résilience Cloud</h3>
    <p><span class="badge badge-blue">Cours Cloud Computing (slides 40 à 47)</span></p>
    <ul>
        <li><strong>Rappel de l'affaire étudiée en cours :</strong> En novembre 2010 ("Cablegate"), Wikileaks publie des milliers de câbles diplomatiques sensibles. Le site subit des attaques DDoS massives (>10 Gbps) rendant ses serveurs indisponibles. Wikileaks migre en urgence sur le Cloud Amazon AWS (EC2/S3), qui absorbe l'attaque grâce à son réseau élastique. Cependant, sous pression politique, Amazon rompt unilatéralement son contrat, et le registrar DNS supprime le nom de domaine <code>wikileaks.org</code>. Wikileaks a dû se rabattre sur des miroirs P2P et des hébergeurs souverains (OVH en France).</li>
        <li><strong>Ce que ce cas démontre pour notre projet :</strong>
            <ol>
                <li><strong>La force du Cloud et des Conteneurs :</strong> La portabilité des conteneurs permet de migrer une application d'un fournisseur à un autre (ou du local vers le cloud) en quelques secondes, sans réécrire le code.</li>
                <li><strong>La protection contre le Lock-In :</strong> En utilisant des manifestes Kubernetes déclaratifs standards plutôt que des services propriétaires fermés, nous évitons la dépendance captive ("Vendor Lock-in") mise en lumière par l'éviction brutale d'Amazon en 2010.</li>
                <li><strong>L'absorption des hausses de trafic :</strong> Grâce à la commande <code>kubectl scale</code> et à l'équilibrage de charge, ContainerLab est conçu pour absorber les augmentations soudaines de requêtes sans tomber en panne.</li>
            </ol>
        </li>
    </ul>

    <h3>3.10 Gestionnaire de Machines Virtuelles (Sandpiper) vs Kubernetes Control Plane</h3>
    <p><span class="badge badge-blue">Cours Virtualisation (slides 34 à 37)</span> <span class="badge badge-blue">Cours Conteneurisation (slides 42 à 46)</span></p>
    <table>
        <thead>
            <tr>
                <th style="width: 20%;">Critère</th>
                <th style="width: 40%;">Gestionnaire de VM classique (Sandpiper - 2009)</th>
                <th style="width: 40%;">Orchestrateur de Conteneurs Moderne (Kubernetes)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Unité d'Orchestration</strong></td>
                <td>Machine Virtuelle complète (OS invité + kernel + disques virtuels de plusieurs Go).</td>
                <td><strong>Pod</strong> : plus petite unité orchestrable, regroupant un ou plusieurs conteneurs légers partageant le même namespace réseau.</td>
            </tr>
            <tr>
                <td><strong>Détection de Surcharge</strong></td>
                <td>Surveille les "hotspots" (nœuds physiques où l'utilisation CPU, RAM ou disque franchit des seuils de saturation).</td>
                <td><strong>Kubelet</strong> et <strong>Metrics Server</strong> surveillent en continu la consommation des Pods par rapport aux <code>requests</code> et <code>limits</code> des cgroups.</td>
            </tr>
            <tr>
                <td><strong>Résolution du Problème</strong></td>
                <td><strong>Live Migration</strong> de la VM vers une autre machine physique moins chargée, via des techniques de <em>Pre-Copy</em> (copie itérative des dirty pages en mémoire) ou <em>Post-Copy</em> (temps de migration réduit mais risque d'état distribué).</td>
                <td><strong>Autoscaling Horizontal (HPA) :</strong> Au lieu de déplacer une VM géante, Kubernetes clone instantanément de nouveaux Pods réplicas sur les nœuds disponibles, et <code>kube-proxy</code> répartit la charge. En cas de panne d'un nœud, le <code>Scheduler</code> replanifie simplement le Pod ailleurs.</td>
            </tr>
        </tbody>
    </table>

    <h3>3.11 Le Lien Direct avec les Travaux Pratiques (LAB-01 EC2 & LAB-02 VPC)</h3>
    <p><span class="badge badge-blue">LAB-01 AWS EC2</span> <span class="badge badge-blue">LAB-02 AWS VPC</span></p>
    <ul>
        <li><strong>Dans le LAB-01 (EC2) :</strong> Vous avez appris à lancer manuellement une machine virtuelle Linux (AMI Amazon Linux 2), à générer une paire de clés privées (.pem / .ppk) pour la connexion sécurisée SSH, à configurer un <strong>Security Group</strong> autorisant les ports 22 (SSH) et 80 (HTTP), et à déployer un serveur web Apache (<code>httpd</code>) via un script User Data.</li>
        <li><strong>Dans le LAB-02 (VPC) :</strong> Vous avez créé un réseau virtuel isolé (VPC en <code>10.0.0.0/16</code>) découpé en deux sous-réseaux :
            <ul>
                <li><strong>Sous-réseau Public :</strong> relié à une <em>Internet Gateway (IGW)</em>, hébergeant les serveurs accessibles depuis Internet (serveur Web).</li>
                <li><strong>Sous-réseau Privé :</strong> sans adresse IP publique, utilisant une <em>passerelle NAT</em> pour ses mises à jour, hébergeant les briques sensibles (serveur de base de données).</li>
            </ul>
        </li>
        <li><strong>Comment ContainerLab concrétise ces LABs :</strong>
            <p>Notre fichier <code>compose.yaml</code> et nos manifestes Kubernetes constituent la <strong>transposition conteneurisée exacte du LAB-02</strong> !</p>
            <ul>
                <li>Notre réseau <code>frontend-net</code> joue le rôle du <strong>sous-réseau public</strong> : seul le conteneur Nginx est exposé vers l'extérieur (port 3000 / 30080).</li>
                <li>Notre réseau <code>backend-net</code> joue le rôle du <strong>sous-réseau privé</strong> : la base de données PostgreSQL ne possède aucune adresse publique et ne peut être jointe que par l'API.</li>
                <li>Nos conteneurs remplacent les lourdes instances EC2 du LAB-01 par des micro-environnements qui s'initialisent en quelques fractions de seconde.</li>
            </ul>
        </li>
    </ul>
    """)
    
    # SECTION 4
    html_parts.append("""
    <div class="page-break"></div>
    <h2>4. L'architecture expliquée simplement & en vrai code</h2>
    <p>Une bonne architecture se reconnaît à ce que <strong>chaque composant a une responsabilité unique et clairement délimitée</strong>. Voici comment les répertoires et les briques de ContainerLab s'articulent :</p>

    <h3>4.1 Arborescence Structurée du Projet</h3>
    <pre><code>c:\\Users\\houss\\Desktop\\Cloud project
├── compose.yaml                      # Définition multi-services Docker Compose (DMZ & volumes)
├── README.md                         # Documentation de référence du projet
│
├── application/                      # Code source applicatif et Dockerfiles
│   ├── frontend/                     # Tier 1 : React 19 SPA + Nginx Reverse Proxy
│   │   ├── Dockerfile                # Multi-stage build optimisé (Node builder -> Nginx runner)
│   │   ├── nginx.conf                # Configuration reverse proxy /api/ et SPA routing
│   │   └── src/App.jsx               # Dashboard d'observabilité et testeur de réplicas
│   ├── backend/                      # Tier 2 : Express REST API (Node.js 24 LTS)
│   │   ├── Dockerfile                # Exécution non-root (USER node) sur Alpine
│   │   ├── src/app.js                # Contrôleurs, sondes liveness/readiness, CRUD annonces
│   │   ├── src/db.js                 # Pool de connexion PostgreSQL (pg.Pool)
│   │   └── test/api.test.js          # Suite de tests unitaires native node:test
│   └── database/                     # Tier 3 : Persistance relationnelle
│       ├── Dockerfile                # Image PostgreSQL 16 Alpine personnalisée
│       └── init.sql                  # Schéma SQL et données d'amorçage automatiques
│
├── kubernetes/                       # 10 Manifestes déclaratifs ordonnés (Namespace containerlab)
│   ├── 00-namespace.yaml             # Frontière administrative logique
│   ├── 01-configmap.yaml             # Variables d'environnement non-sensibles
│   ├── 02-api-secret.yaml            # Identifiants de base de données (type: Opaque)
│   ├── 03-database-pvc.yaml          # Réclamation de volume persistant 1Gi (StorageClass standard)
│   ├── 04-database-deployment.yaml   # Pod PostgreSQL 16 avec strategy: Recreate
│   ├── 05-database-service.yaml      # Service interne ClusterIP (port 5432)
│   ├── 06-api-deployment.yaml        # Déploiement API Express (2 réplicas, sondes, cgroups limits)
│   ├── 07-api-service.yaml           # Service interne ClusterIP load-balancer (port 5000)
│   ├── 08-frontend-deployment.yaml   # Déploiement web React + Nginx
│   └── 09-frontend-service.yaml      # Service externe NodePort (port statique 30080)
│
└── scripts/                          # Automatisation PowerShell 7+
    ├── build-images.ps1              # Construction des images Docker versionnées (v1.0.0)
    ├── benchmark-images.ps1          # Mesure automatisée des gains de taille (Test T02)
    ├── run-compose.ps1               # Démarrage orchestré de Docker Compose
    ├── deploy-k8s.ps1                # Déploiement séquentiel dans Minikube
    ├── run-tests.ps1                 # Suite d'orchestration end-to-end T01 à T11
    └── cleanup.ps1                   # Nettoyage complet des conteneurs et du cluster</code></pre>

    <h3>4.2 Schéma d'Architecture & Flux Réseau</h3>
    <div class="diagram-box">
+-----------------------------------------------------------------------------------------+
|                                      NAVIGATEUR CLIENT                                  |
+-----------------------------------------------------------------------------------------+
                                             |
                                             | HTTP (Compose: :3000 | Minikube NodePort: :30080)
                                             v
+-----------------------------------------------------------------------------------------+
|                              TIER 1: FRONTEND & REVERSE PROXY                           |
|  - Conteneur: Nginx stable-alpine-slim servant le bundle statique React 19              |
|  - Réseau: frontend-net (Docker Compose) / namespace containerlab (Kubernetes)          |
|  - Règle Proxy Interne: location /api/ { proxy_pass http://api:5000/api/; }             |
+-----------------------------------------------------------------------------------------+
                                             |
                                             | DNS Interne: http://api:5000/api/*
                                             v
+-----------------------------------------------------------------------------------------+
|                              TIER 2: BACKEND REST API                                   |
|  - Conteneur: Node.js 24 LTS Express API exécuté en non-root ('USER node')              |
|  - Réplicas: 2 Pods (extensible à 4 via kubectl scale)                                  |
|  - Endpoints:                                                                           |
|      * GET  /api/health/live    -> Sonde de vivacité (Liveness : boucle d'événements)   |
|      * GET  /api/health/ready   -> Sonde de préparation (Readiness : pool PostgreSQL)   |
|      * GET  /api/instance       -> Nom d'hôte & Pod ID pour le suivi des réplicas       |
|      * GET  /api/announcements  -> Lecture des annonces en base                         |
|      * POST /api/announcements  -> Insertion d'une annonce en base                      |
+-----------------------------------------------------------------------------------------+
                                             |
                                             | TCP 5432 (DNS Interne: postgres:5432)
                                             v
+-----------------------------------------------------------------------------------------+
|                              TIER 3: DATABASE & PERSISTANCE                             |
|  - Conteneur: PostgreSQL 16 Alpine avec init.sql automatique                            |
|  - Stockage: PersistentVolumeClaim (1Gi) / Volume nommé postgres_data                    |
|  - Stratégie K8s: { type: Recreate } (évite le verrouillage multi-attach ReadWriteOnce) |
|  - Isolation: backend-net uniquement (inaccessible depuis le Frontend sous Compose)     |
+-----------------------------------------------------------------------------------------+
    </div>

    <h3>4.3 Le Trajet d'une Requête de Bout en Bout (Exemple : Créer une Annonce)</h3>
    <ol>
        <li><strong>Action utilisateur :</strong> Sur le dashboard React, l'utilisateur remplit le formulaire et clique sur <em>"Publier l'annonce"</em>. La fonction <code>fetch('/api/announcements', { method: 'POST', body: ... })</code> est déclenchée.</li>
        <li><strong>Arrivée sur le port externe :</strong> La requête HTTP arrive sur le port publié de l'hôte (<code>3000</code> en Compose, ou <code>30080</code> en Minikube).</li>
        <li><strong>Routage Nginx (Tier 1) :</strong> Le serveur web Nginx reçoit la requête. La directive <code>location /api/</code> de <code>nginx.conf</code> intercepte l'appel et effectue un reverse proxy transparent vers le nom d'hôte interne :
            <pre><code>location /api/ {
    proxy_pass http://api:5000/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}</code></pre>
        </li>
        <li><strong>Traitement API Express (Tier 2) :</strong> Le serveur Node.js reçoit la requête sur le port 5000 :
            <ul>
                <li>Le middleware de journalisation note la requête avec le nom d'hôte du pod (<code>os.hostname()</code>).</li>
                <li>Le contrôleur valide que les champs <code>title</code> et <code>content</code> ne sont pas vides, supprime les espaces superflus (<code>trim()</code>), et vérifie les plafonds (150 caractères pour le titre, 2000 pour le contenu).</li>
            </ul>
            <pre><code>// Extrait de application/backend/src/app.js
const result = await db.query(
  'INSERT INTO announcements (title, content, author) VALUES ($1, $2, $3) RETURNING *;',
  [title, content, author]
);
res.status(201).json({ success: true, podName: os.hostname(), data: result.rows[0] });</code></pre>
        </li>
        <li><strong>Persistance PostgreSQL (Tier 3) :</strong> Le client PostgreSQL (<code>pg.Pool</code>) envoie la requête paramétrée sur le port 5432. PostgreSQL écrit la ligne dans la table <code>announcements</code>, dont les données résident physiquement sur le volume persistant.</li>
        <li><strong>Retour de la réponse :</strong> L'API répond avec le code HTTP <code>201 Created</code> et le nom du Pod ayant traité l'opération. Nginx retransmet le JSON au navigateur. Le composant React met à jour le fil d'annonces instantanément sans recharger la page.</li>
    </ol>

    <h3>4.4 Le Grand Secret d'Architecture : Pourquoi Nginx en Reverse Proxy ?</h3>
    <div class="callout callout-warning">
        <div class="callout-title">⚠️ Question Piège n°1 des Professeures à la Soutenance !</div>
        <em>"Pourquoi ne pas appeler directement http://api:5000 depuis votre code React dans le navigateur ?"</em>
    </div>
    <p>Voici l'explication technique que le jury attend :</p>
    <p>Une application React (Single Page Application) est compilée en amont en fichiers HTML et JavaScript statiques. <strong>Ce code JavaScript ne s'exécute PAS dans un conteneur sur le serveur, mais directement dans le moteur JavaScript du navigateur web de l'utilisateur, sur la machine hôte Windows.</strong></p>
    <p>Or, le système d'exploitation de la machine hôte est <strong>totalement incapable de résoudre les noms d'hôtes internes</strong> du réseau Docker ou du cluster Kubernetes (comme <code>http://api:5000</code> ou <code>http://postgres:5432</code>), car ces noms sont résolus par le serveur DNS interne de Docker (127.0.0.11) ou CoreDNS dans Kubernetes, accessibles uniquement <em>depuis l'intérieur des conteneurs</em>.</p>
    <p>Si le code React appelait <code>http://api:5000</code>, la requête échouerait immédiatement avec l'erreur <code>ERR_NAME_NOT_RESOLVED</code>.</p>
    <p>En plaçant <strong>Nginx en reverse proxy</strong> dans le conteneur frontend :</p>
    <ul>
        <li><strong>Résolution de même origine (Same-Origin) :</strong> Le navigateur envoie toutes ses requêtes sur la même adresse et le même port que le site web (<code>/api/*</code>). Zéro problème de CORS (Cross-Origin Resource Sharing) !</li>
        <li><strong>Sécurité maximale :</strong> Un seul port public est ouvert sur l'hôte (port 3000 ou 30080). Les ports de l'API (5000) et de PostgreSQL (5432) restent 100% privés et inaccessibles depuis l'extérieur.</li>
        <li><strong>Portabilité absolue :</strong> La configuration fonctionne à l'identique sous Docker Compose et sous Kubernetes sans changer une seule ligne de code côté frontend.</li>
    </ul>

    <h3>4.5 L'Isolation DMZ sous Docker Compose</h3>
    <p>Dans <code>compose.yaml</code>, nous avons rejeté le réseau par défaut unique pour configurer deux réseaux bridge segmentés :</p>
    <pre><code># compose.yaml (extrait de segmentation)
services:
  frontend:
    networks:
      - frontend-net    # Accède à l'API uniquement
  api:
    networks:
      - frontend-net    # Rejoint le frontend
      - backend-net     # Rejoint la base de données
  postgres:
    networks:
      - backend-net     # Isolé ! Inaccessible depuis frontend-net

networks:
  frontend-net:
    driver: bridge
  backend-net:
    driver: bridge</code></pre>
    <p><strong>Preuve formelle d'isolation :</strong> Si un assaillant compromettait le serveur Nginx dans le conteneur frontend et tentait de contacter directement PostgreSQL :</p>
    <pre><code>docker exec containerlab-frontend ping postgres
# Résultat : Ping request could not find host postgres. Isolation validée !</code></pre>

    <h3>4.6 Sécurité des Conteneurs : Utilisateur Non-Root & Secrets Découplés</h3>
    <ul>
        <li><strong>Exécution non-root (<code>USER node</code>) :</strong> Par défaut, un conteneur Docker s'exécute avec les privilèges <code>root</code>. Si une faille d'exécution de code à distance (RCE) survient dans l'API, l'attaquant possède les droits root dans le conteneur et peut tenter une évasion de noyau. Dans <code>application/backend/Dockerfile</code>, nous forçons l'instruction <code>USER node</code> (UID standard 1000). Le processus Node.js s'exécute sans aucun droit d'administration système.</li>
        <li><strong>Découplage Configuration / Secrets :</strong> Aucune chaîne de connexion ni mot de passe n'est écrit en dur dans le code source. Les variables de configuration non sensibles (noms de tables, ports) sont injectées par le <code>ConfigMap</code> (<code>01-configmap.yaml</code>), et les identifiants d'accès PostgreSQL sont injectés via un <code>Secret</code> Kubernetes (<code>02-api-secret.yaml</code>).</li>
    </ul>
    """)
    
    # SECTION 5
    html_parts.append("""
    <div class="page-break"></div>
    <h2>5. La démo pas à pas (Scénario chronométré 8 à 10 minutes)</h2>
    <p>Une soutenance réussie est une <strong>démonstration vivante, rythmée et scénarisée</strong>. Ne récitez pas de la théorie dans le vide : appuyez chaque phrase sur une action visible à l'écran.</p>

    <h3>Organisation & Répartition des Rôles du Binôme</h3>
    <ul>
        <li><strong>Houssem Sassi (Étudiant 1) :</strong> Prend le lead sur la présentation générale, la composition locale Docker Compose, l'ingénierie des Dockerfiles et les benchmarks d'optimisation. Réalise les deux crash-tests (auto-guérison et persistance PVC).</li>
        <li><strong>Nour El Houde Jaziri (Étudiant 2) :</strong> Prend le lead sur le déploiement Kubernetes, l'explication des manifestes déclaratifs, l'utilisation du dashboard d'observabilité, la démonstration du scaling horizontal (2 à 4 réplicas) et la projection cloud AWS.</li>
    </ul>

    <h3>Préparation de l'Environnement (15 minutes avant le passage)</h3>
    <ol>
        <li>Ouvrir <strong>Docker Desktop</strong> et vérifier que le moteur est en cours d'exécution.</li>
        <li>Ouvrir un premier terminal PowerShell 7 et démarrer Minikube : <code>minikube start --driver=docker</code>.</li>
        <li>Précharger les images dans Minikube : <code>.\\scripts\\load-images.ps1</code>.</li>
        <li>Ouvrir un second terminal scindé pour surveiller en direct l'état des Pods :
            <pre><code>kubectl get pods -n containerlab -w</code></pre>
        </li>
        <li>Ouvrir le navigateur web sur <code>http://localhost:3000</code> (Compose) ou l'URL NodePort (Minikube).</li>
    </ol>

    <h3>Le Scénario Chronométré Minute par Minute</h3>

    <div class="step-box">
        <div class="step-header">
            <span>Étape 1 : Cadrage Académique & Objectif du Projet</span>
            <span>0:00 - 1:00 · Houssem</span>
        </div>
        <p><strong>Action :</strong> Afficher la page d'accueil de la console web ou le README du projet.<br>
        <strong>Ce qu'on dit :</strong> <em>"Bonjour Madame. Dans le cadre du cours de Virtualisation et Cloud Computing, nous avons choisi la Proposition 2 : Conteneurisation et Orchestration locale vs Cloud. Notre projet ContainerLab matérialise le passage de la virtualisation lourde à la conteneurisation légère à travers une application 3-tiers résiliente (React, Node.js Express, PostgreSQL). Nous allons vous démontrer son orchestration sous Docker Compose puis sous Kubernetes sur Minikube, validée par notre suite de tests T01 à T11."</em></p>
    </div>

    <div class="step-box">
        <div class="step-header">
            <span>Étape 2 : Démonstration Docker Compose & Isolation DMZ</span>
            <span>1:00 - 2:30 · Houssem</span>
        </div>
        <p><strong>Action :</strong> Dans le terminal, exécuter <code>.\\scripts\\run-compose.ps1</code> puis <code>docker compose ps</code>.<br>
        <strong>Ce qu'on montre :</strong> Les trois services <code>containerlab-frontend</code>, <code>containerlab-api</code> et <code>containerlab-postgres</code> affichent le statut <code>Up (healthy)</code>.<br>
        <strong>Ce qu'on dit :</strong> <em>"Sous Docker Compose, nous avons mis en place deux réseaux bridge distincts : frontend-net et backend-net. L'API est la seule passerelle entre les deux. La base de données PostgreSQL est totalement invisible pour le frontend, ce qui empêche toute attaque directe sur le port 5432. De plus, nos dépendances sont synchronisées par des sondes de santé conditionnelles (condition: service_healthy) : l'API attend que PostgreSQL soit réellement prêt (pg_isready) avant de démarrer."</em></p>
        <div class="screenshot-container">
            <img class="screenshot-img" src='""" + img_compose + """' alt='Validation Docker Compose' />
            <div class="screenshot-caption">Figure 2 : Validation officielle de l'orchestration sous Docker Compose : 3 conteneurs en statut Up (healthy) avec DMZ frontend-net / backend-net.</div>
        </div>
    </div>

    <div class="step-box">
        <div class="step-header">
            <span>Étape 3 : Benchmarks d'Optimisation des Dockerfiles (3 Pts du Barème)</span>
            <span>2:30 - 3:30 · Houssem</span>
        </div>
        <p><strong>Action :</strong> Ouvrir <code>docs/benchmarks/image-sizes.md</code> ou exécuter <code>.\\scripts\\benchmark-images.ps1</code>.<br>
        <strong>Ce qu'on montre :</strong> Le tableau comparatif montrant la réduction de l'image Frontend de 80.92 MB à 5.56 MB.<br>
        <strong>Ce qu'on dit :</strong> <em>"Pour répondre à l'axe 1 du barème, nous avons conçu des Dockerfiles de production. Pour le frontend, nous utilisons un Multi-Stage Build : le stage builder utilise Node 24 pour compiler le JSX, puis le stage runner copie uniquement le dossier compilé dist/ dans une image Nginx ultra-légère. Résultat mesuré : une réduction de 93.1% de la taille d'image, soit plus de 75 Mo d'outils inutiles éliminés. Côté backend, nous appliquons USER node pour interdire l'exécution en root."</em></p>
    </div>

    <div class="step-box">
        <div class="step-header">
            <span>Étape 4 : Déploiement Déclaratif Kubernetes sur Minikube (5 Pts du Barème)</span>
            <span>3:30 - 4:45 · Nour</span>
        </div>
        <p><strong>Action :</strong> Exécuter <code>.\\scripts\\deploy-k8s.ps1</code> puis <code>kubectl get all,pvc -n containerlab</code>.<br>
        <strong>Ce qu'on montre :</strong> Le Namespace <code>containerlab</code> créé, le PVC en statut <code>Bound</code>, et les 4 Pods en statut <code>Running (1/1 Ready)</code>.<br>
        <strong>Ce qu'on dit :</strong> <em>"Nous passons maintenant à l'orchestration de cluster avec Kubernetes. Nous appliquons 10 manifestes déclaratifs numérotés de 00 à 09. Nous isolons notre application dans le Namespace containerlab. La configuration et les mots de passe sont découplés via ConfigMap et Secret. Les briques internes communiquent via des Services ClusterIP, tandis que le frontend est exposé à l'extérieur par un Service NodePort sur le port 30080."</em></p>
    </div>

    <div class="step-box">
        <div class="step-header">
            <span>Étape 5 : Navigation sur le Dashboard & Test Inter-Tiers</span>
            <span>4:45 - 6:00 · Nour</span>
        </div>
        <p><strong>Action :</strong> Basculer sur le navigateur web. Constater les voyants verts (Frontend, API, DB). Remplir le formulaire et publier une annonce <em>"Test Soutenance ESSTHS 2026"</em>.<br>
        <strong>Ce qu'on montre :</strong> L'annonce apparaît immédiatement dans le fil, et le badge <code>Serving Replica</code> affiche le nom du Pod API qui a traité la requête.<br>
        <strong>Ce qu'on dit :</strong> <em>"Voici notre console d'observabilité. Elle interroge l'endpoint /api/instance pour afficher en direct le Pod Kubernetes qui répond. Quand nous ajoutons une annonce, la requête traverse le reverse proxy Nginx, est validée par l'API Express, et s'écrit dans la base PostgreSQL hébergée sur notre volume persistant."</em></p>
    </div>

    <div class="step-box">
        <div class="step-header">
            <span>Étape 6 : MOMENT FORT 1 — Scaling Horizontal & Répartition de Charge</span>
            <span>6:00 - 7:00 · Nour</span>
        </div>
        <p><strong>Action :</strong> Dans le terminal, exécuter :
        <pre><code>kubectl scale deployment/api --replicas=4 -n containerlab
kubectl get pods -l app=api -n containerlab</code></pre>
        Revenir sur le dashboard et cliquer sur <strong>"Send 6 Calls"</strong> (Tester la répartition).<br>
        <strong>Ce qu'on montre :</strong> Les 4 Pods passent immédiatement à <code>Running</code>. Les résultats des 6 requêtes affichent des noms de Pods différents en alternance !<br>
        <strong>Ce qu'on dit :</strong> <em>"Regardez : nous avons augmenté la capacité de l'API de 2 à 4 réplicas en une seconde. Le contrôleur ReplicaSet a instantanément programmé les nouveaux Pods. En cliquant sur le test de charge, kube-proxy distribue automatiquement le trafic entre les 4 réplicas selon ses règles iptables. C'est l'illustration exacte de l'élasticité cloud vue en cours !"</em></p>
    </div>

    <div class="step-box">
        <div class="step-header">
            <span>Étape 7 : MOMENT FORT 2 — Crash-Test d'Auto-Guérison (Self-Healing)</span>
            <span>7:00 - 8:00 · Houssem</span>
        </div>
        <p><strong>Action :</strong> Copier le nom du Pod actif affiché sur le dashboard (ex: <code>api-7d498b58f9-k2x89</code>). Dans le terminal, exécuter :
        <pre><code>kubectl delete pod &lt;nom-du-pod&gt; -n containerlab --now</code></pre>
        Montrer le terminal de monitoring et rafraîchir le dashboard.<br>
        <strong>Ce qu'on montre :</strong> Le Pod supprimé disparaît, un nouveau Pod est créé en 1.5 seconde, et le dashboard continue de répondre sans aucune interruption de service.<br>
        <strong>Ce qu'on dit :</strong> <em>"Voici l'auto-guérison autonome de Kubernetes. Même si nous détruisons brutalement un Pod API en production, la boucle de réconciliation du ReplicaSet détecte l'écart entre l'état désiré (4 réplicas) et l'état réel (3 réplicas). Un Pod de remplacement est immédiatement instancié et rattaché au Service, garantissant une haute disponibilité sans intervention humaine."</em></p>
    </div>

    <div class="step-box">
        <div class="step-header">
            <span>Étape 8 : MOMENT FORT 3 — Persistance des Données après Crash de la Base</span>
            <span>8:00 - 9:00 · Houssem</span>
        </div>
        <p><strong>Action :</strong> Dans le terminal, supprimer le Pod PostgreSQL :
        <pre><code>kubectl delete pod -l app=postgres -n containerlab --now</code></pre>
        Attendre 4 secondes que le contrôleur recrée le Pod, puis recharger la page web.<br>
        <strong>Ce qu'on montre :</strong> L'annonce <em>"Test Soutenance ESSTHS 2026"</em> est toujours présente dans la liste !<br>
        <strong>Ce qu'on dit :</strong> <em>"C'est la démonstration de la gestion des volumes (Axe 4). Les conteneurs sont éphémères, mais pas notre stockage : grâce au PersistentVolumeClaim et à notre stratégie Recreate, le nouveau Pod PostgreSQL s'est reconnecté au même volume persistant sans conflit de verrouillage. Zéro perte de données !"</em></p>
    </div>

    <div class="step-box">
        <div class="step-header">
            <span>Étape 9 : Projection Cloud d'Entreprise AWS & Comparaison ECS</span>
            <span>9:00 - 9:45 · Nour</span>
        </div>
        <p><strong>Action :</strong> Projeter le schéma d'architecture AWS de <code>docs/aws-comparison.md</code>.<br>
        <strong>Ce qu'on montre :</strong> Le diagramme d'architecture VPC Multi-AZ avec ALB, EKS / ECS Fargate et Amazon RDS.<br>
        <strong>Ce qu'on dit :</strong> <em>"Pour passer de notre cluster local Minikube à la production sur AWS, nous transposerions nos briques : Minikube devient Amazon EKS ou Amazon ECS avec AWS Fargate sans serveur. Notre NodePort devient un Application Load Balancer (ALB) avec terminaison SSL et AWS WAF. Et pour la base, au lieu d'un conteneur avec PVC, la bonne pratique cloud est d'utiliser Amazon RDS PostgreSQL managé avec réplication synchrone Multi-AZ et basculement automatique en moins de 60 secondes."</em></p>
    </div>

    <div class="step-box">
        <div class="step-header">
            <span>Étape 10 : Conclusion & Ouverture aux Questions</span>
            <span>9:45 - 10:00 · Houssem & Nour</span>
        </div>
        <p><strong>Ce qu'on dit :</strong> <em>"En conclusion, ContainerLab valide l'ensemble des compétences de la Proposition 2 : Dockerfiles optimisés (-93%), composition sécurisée en DMZ, déploiement déclaratif sur Kubernetes, scalabilité horizontale, self-healing et persistance sans faille. Nous vous remercions pour votre écoute et nous sommes prêts à répondre à vos questions."</em></p>
    </div>

    <h3>Plan B : Que faire si un incident survient pendant la démo ?</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 25%;">Incident Possible</th>
                <th style="width: 35%;">Cause Probable</th>
                <th style="width: 40%;">Solution Immédiate (Moins de 10 secondes)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Port 3000 déjà utilisé</strong></td>
                <td>Une ancienne instance de Docker Compose ou un process Node tourne en arrière-plan.</td>
                <td>Exécuter <code>.\\scripts\\cleanup.ps1</code> ou <code>docker compose down</code>, puis relancer <code>.\\scripts\\run-compose.ps1</code>.</td>
            </tr>
            <tr>
                <td><strong>Minikube ne répond pas</strong></td>
                <td>Le cluster Minikube a été mis en pause ou Docker Desktop a redémarré.</td>
                <td>Exécuter <code>minikube status</code>. Si arrêté, lancer <code>minikube start --driver=docker</code>.</td>
            </tr>
            <tr>
                <td><strong>Erreur ImagePullBackOff</strong></td>
                <td>Les images n'ont pas été chargées dans le cache interne de Minikube.</td>
                <td>Exécuter immédiatement <code>.\\scripts\\load-images.ps1</code> (charge les images locales sans passer par Internet).</td>
            </tr>
            <tr>
                <td><strong>La base met du temps à répondre</strong></td>
                <td>PostgreSQL est en cours d'initialisation du volume (<code>init.sql</code>).</td>
                <td>Montrer la sonde <code>/api/health/ready</code> qui renvoie 503 : expliquer que le découplage protège le cluster en attendant que la base soit prête !</td>
            </tr>
        </tbody>
    </table>
    """)
    
    # SECTION 6
    html_parts.append("""
    <div class="page-break"></div>
    <h2>6. Les 8 règles d'or d'ingénierie à connaître par cœur</h2>
    <p>Ces huit règles sont les choix techniques majeurs qui font la solidité professionnelle de ContainerLab. Si vous savez les énoncer et expliquer leur raison d'être, vous démontrez une maturité d'ingénieur remarquable :</p>

    <div class="callout callout-info">
        <div class="callout-title">Règle 1 : Multi-Stage Build obligatoire pour les applications compilées</div>
        <strong>Pourquoi :</strong> Dans une application React ou Angular, les compilateurs (Node.js, Vite, npm) ne servent qu'au moment de la fabrication (build). Les inclure dans l'image finale augmente la surface d'attaque et multiplie le poids de l'image par 15. En ne copiant que le dossier <code>dist/</code> dans <code>nginx:stable-alpine-slim</code>, l'image passe de <strong>80.92 MB à 5.56 MB (-93.1%)</strong>.
    </div>

    <div class="callout callout-danger">
        <div class="callout-title">Règle 2 : Stratégie 'Recreate' impérative pour les bases de données sur volume ReadWriteOnce</div>
        <strong>Pourquoi :</strong> Par défaut, un Déploiement Kubernetes utilise la stratégie <code>RollingUpdate</code> (il démarre le nouveau Pod avant de tuer l'ancien pour assurer le zéro downtime). Mais un volume persistant EBS ou HostPath est de type <code>ReadWriteOnce</code> (un seul nœud/pod peut monter le disque en écriture à la fois). Si Kubernetes lance le nouveau Pod DB alors que l'ancien n'est pas encore éteint, le montage échoue avec l'erreur bloquante <code>Multi-Attach error for volume</code>. Définir <code>strategy: { type: Recreate }</code> dans <code>04-database-deployment.yaml</code> force Kubernetes à éteindre l'ancien Pod avant de monter le disque sur le nouveau.
    </div>

    <div class="callout callout-warning">
        <div class="callout-title">Règle 3 : Découpler strictement la sonde de vie (Liveness) et la sonde de préparation (Readiness)</div>
        <strong>Pourquoi :</strong> La sonde de vivacité (<code>/api/health/live</code>) teste uniquement si le processus Node.js tourne. La sonde de préparation (<code>/api/health/ready</code>) teste si la connexion à PostgreSQL est active. Si l'on mettait le test de base de données dans la sonde de vivacité, un simple redémarrage temporaire de PostgreSQL entraînerait l'échec de la sonde de vie de l'API : Kubernetes tuerait alors tous les Pods API en boucle, provoquant un <strong>redémarrage en cascade catastrophique</strong> ! Avec notre découplage, si la base redémarre, l'API échoue seulement à sa Readiness probe : Kubernetes retire temporairement le Pod de l'équilibreur sans le tuer, jusqu'au retour de la base.
    </div>

    <div class="callout callout-info">
        <div class="callout-title">Règle 4 : 'imagePullPolicy: Never' et versionnement sémantique strict en local</div>
        <strong>Pourquoi :</strong> Si une image utilise le tag <code>latest</code>, Kubernetes applique par défaut la politique <code>imagePullPolicy: Always</code> et cherche à télécharger l'image sur Docker Hub. Sur une machine locale ou sans connexion Internet, le déploiement échoue avec <code>ErrImagePull</code>. En utilisant des tags précis (<code>v1.0.0</code>) et la directive <code>imagePullPolicy: Never</code>, nous garantissons une évaluation 100% hors-ligne et reproductible depuis le cache Minikube.
    </div>

    <div class="callout callout-success">
        <div class="callout-title">Règle 5 : Exécution sous utilisateur non-root ('USER node')</div>
        <strong>Pourquoi :</strong> Le noyau Linux partage ses tables d'UID entre l'hôte et les conteneurs. Exécuter un conteneur en <code>root</code> expose la machine hôte à des attaques d'élévation de privilèges en cas de faille applicative. L'instruction <code>USER node</code> dans <code>application/backend/Dockerfile</code> confine l'application dans un compte sans droit sudo.
    </div>

    <div class="callout callout-purple">
        <div class="callout-title">Règle 6 : Un Namespace Kubernetes est une frontière administrative, pas un pare-feu réseau</div>
        <strong>Pourquoi :</strong> Beaucoup de candidats commettent l'erreur de croire qu'isoler des Pods dans le Namespace <code>containerlab</code> empêche les autres Pods du cluster de leur parler. C'est faux : par défaut, le réseau Kubernetes est plat (flat network). L'isolation réseau stricte exige des ressources <code>NetworkPolicy</code> associées à un CNI compatible (Calico, Cilium). Dans notre projet, l'isolation réseau physique est démontrée sous Docker Compose via les réseaux bridge étanches.
    </div>

    <div class="callout callout-info">
        <div class="callout-title">Règle 7 : Synchronisation déterministe au démarrage ('condition: service_healthy')</div>
        <strong>Pourquoi :</strong> Par défaut, Docker Compose lance les conteneurs en parallèle. Un conteneur PostgreSQL met plusieurs secondes à initialiser ses fichiers de données et exécuter <code>init.sql</code>. Si l'API démarre en même temps, elle tente de se connecter à un port 5432 fermé et crashe. La clause <code>depends_on: { postgres: { condition: service_healthy } }</code> oblige l'API à attendre le code retour succès de <code>pg_isready</code>.
    </div>

    <div class="callout callout-info">
        <div class="callout-title">Règle 8 : Service NodePort 30080 pour l'évaluation autonome</div>
        <strong>Pourquoi :</strong> Sur un cluster de production AWS, l'accès externe se fait via un Ingress Controller relié à un Application Load Balancer (ALB). En environnement local Minikube sur Windows, le contrôleur Ingress nécessite l'activation de tunnels ou de modules complémentaires souvent instables. Utiliser un service <code>NodePort</code> sur le port fixe <code>30080</code> assure une démonstration infaillible, sans dépendance externe.
    </div>
    """)
    
    # SECTION 7
    html_parts.append("""
    <div class="page-break"></div>
    <h2>7. La suite de tests automatisée et ce qu'elle prouve vraiment</h2>
    <p>La rigueur d'un projet d'ingénierie se mesure à sa capacité d'être vérifié automatiquement. ContainerLab intègre <strong>deux niveaux de tests complémentaires</strong> :</p>

    <h3>7.1 Tests Unitaires Applicatifs (Tier 2 API)</h3>
    <p>Exécutés dans <code>application/backend</code> via le test-runner natif de Node.js (<code>node:test</code> et <code>node:assert</code>) avec la commande <code>npm test</code>. Ils s'exécutent en isolation sans nécessiter que Docker ou la base de données soient lancés :</p>
    <ul>
        <li><strong>Vérification 1 :</strong> <code>GET /api/health/live</code> renvoie HTTP 200 avec le statut <code>alive</code>, le nom d'hôte et l'uptime.</li>
        <li><strong>Vérification 2 :</strong> <code>GET /api/instance</code> renvoie HTTP 200 avec les métadonnées de plateforme et l'empreinte mémoire.</li>
        <li><strong>Vérification 3 :</strong> <code>POST /api/announcements</code> sans titre ni contenu est rejeté avec HTTP 400.</li>
        <li><strong>Vérification 4 :</strong> <code>POST /api/announcements</code> avec des chaînes d'espaces blancs uniquement (<code>"   "</code>) est assaini et rejeté avec HTTP 400.</li>
        <li><strong>Vérification 5 :</strong> <code>POST /api/announcements</code> dont le titre dépasse 150 caractères est rejeté avec HTTP 400.</li>
        <li><strong>Vérification 6 :</strong> <code>GET /api/announcements?limit=abc</code> avec un paramètre invalide est rejeté avec HTTP 400.</li>
        <li><strong>Vérification 7 :</strong> Route inexistante (<code>GET /api/nonexistent</code>) renvoie HTTP 404 propre.</li>
    </ul>

    <h3>7.2 La Matrice d'Orchestration End-to-End : Tests T01 à T11</h3>
    <p>Automatisée par le script PowerShell <code>scripts/run-tests.ps1</code> avec assertions strictes sur les codes de sortie. Tous les tests ont été exécutés et validés avec succès :</p>

    <table>
        <thead>
            <tr>
                <th style="width: 8%;">ID</th>
                <th style="width: 12%;">Niveau</th>
                <th style="width: 25%;">Scénario Testé</th>
                <th style="width: 35%;">Procédure & Commande</th>
                <th style="width: 20%;">Résultat Validé</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Unit</strong></td>
                <td>Applicatif</td>
                <td>Validation unitaire API Express</td>
                <td><code>npm test</code> dans <code>application/backend</code></td>
                <td><span class="badge badge-green">7/7 réussis</span> Code 0</td>
            </tr>
            <tr>
                <td><strong>T01</strong></td>
                <td>Build</td>
                <td>Construction des images multi-stage</td>
                <td><code>.\\scripts\\build-images.ps1</code></td>
                <td><span class="badge badge-green">3 images v1.0.0</span> créées</td>
            </tr>
            <tr>
                <td><strong>T02</strong></td>
                <td>Optimisation</td>
                <td>Benchmark d'optimisation d'image</td>
                <td><code>.\\scripts\\benchmark-images.ps1</code></td>
                <td><span class="badge badge-green">-93.1% Frontend</span> (5.56 Mo)</td>
            </tr>
            <tr>
                <td><strong>T03</strong></td>
                <td>Compose</td>
                <td>Orchestration locale multi-services</td>
                <td><code>.\\scripts\\run-compose.ps1</code></td>
                <td><span class="badge badge-green">3 services healthy</span></td>
            </tr>
            <tr>
                <td><strong>T04</strong></td>
                <td>Compose</td>
                <td>Communication inter-tiers (CRUD)</td>
                <td>Insertion REST <code>POST /api/announcements</code></td>
                <td><span class="badge badge-green">HTTP 201</span> Donnée stockée</td>
            </tr>
            <tr>
                <td><strong>T05</strong></td>
                <td>Compose</td>
                <td>Persistance du volume nommé</td>
                <td><code>docker compose restart postgres</code></td>
                <td><span class="badge badge-green">Donnée conservée</span></td>
            </tr>
            <tr>
                <td><strong>T06</strong></td>
                <td>K8s</td>
                <td>Déploiement déclaration sur Minikube</td>
                <td><code>.\\scripts\\deploy-k8s.ps1</code></td>
                <td><span class="badge badge-green">4 Pods Ready</span>, PVC Bound</td>
            </tr>
            <tr>
                <td><strong>T07</strong></td>
                <td>K8s</td>
                <td>Équilibrage de charge (Load Balancing)</td>
                <td>10 requêtes consécutives à <code>/api/instance</code></td>
                <td><span class="badge badge-green">2 Pods alternés</span> (6 et 4)</td>
            </tr>
            <tr>
                <td><strong>T08</strong></td>
                <td>K8s</td>
                <td>Scaling horizontal des réplicas</td>
                <td><code>kubectl scale deployment api --replicas=4</code></td>
                <td><span class="badge badge-green">4 réplicas Ready</span></td>
            </tr>
            <tr>
                <td><strong>T09</strong></td>
                <td>K8s</td>
                <td>Auto-guérison (Self-Healing)</td>
                <td><code>kubectl delete pod &lt;api-pod&gt; --now</code></td>
                <td><span class="badge badge-green">Pod recréé</span> en &lt; 2s</td>
            </tr>
            <tr>
                <td><strong>T10</strong></td>
                <td>K8s</td>
                <td>Persistance du PVC PostgreSQL</td>
                <td><code>kubectl delete pod &lt;postgres-pod&gt; --now</code></td>
                <td><span class="badge badge-green">Données intactes</span> au reboot</td>
            </tr>
            <tr>
                <td><strong>T11</strong></td>
                <td>Cleanup</td>
                <td>Démontage propre de l'infrastructure</td>
                <td><code>.\\scripts\\cleanup.ps1</code></td>
                <td><span class="badge badge-green">Cluster propre</span> (Code 0)</td>
            </tr>
        </tbody>
    </table>

    <div class="screenshot-container">
        <img class="screenshot-img" src='""" + img_k8s + """' alt='Preuve Kubernetes' />
        <div class="screenshot-caption">Figure 3 : Capture d'écran officielle attestant du bon fonctionnement du cluster Kubernetes : Pods en statut Running, PVC en statut Bound et services ClusterIP/NodePort configurés.</div>
    </div>
    """)
    
    # SECTION 8
    html_parts.append("""
    <div class="page-break"></div>
    <h2>8. Les bugs réels rencontrés, pièges évités et leçons apprises</h2>
    <p>Expliquer les difficultés surmontées démontre au jury que vous maîtrisez le code et que vous ne vous êtes pas contentés de copier un modèle :</p>

    <table>
        <thead>
            <tr>
                <th style="width: 18%;">Symptôme / Erreur</th>
                <th style="width: 25%;">Cause Technique Profonde</th>
                <th style="width: 32%;">Correction Appliquée</th>
                <th style="width: 25%;">Leçon d'Ingénierie</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Multi-Attach error for volume</strong> lors de la mise à jour de PostgreSQL</td>
                <td>Le volume persistant Minikube est <code>ReadWriteOnce</code>. Avec la stratégie par défaut <code>RollingUpdate</code>, le nouveau Pod tente de monter le disque alors que l'ancien le détient encore.</td>
                <td>Configuration explicite de <code>strategy: { type: Recreate }</code> dans <code>04-database-deployment.yaml</code>.</td>
                <td>Un volume RWO ne peut avoir qu'un seul montage en écriture à la fois : toujours éteindre avant de remonter.</td>
            </tr>
            <tr>
                <td><strong>ERR_NAME_NOT_RESOLVED</strong> sur les appels <code>http://api:5000</code></td>
                <td>Le code JavaScript React tourne dans le navigateur de l'hôte Windows. L'hôte ne peut pas résoudre les noms DNS internes du réseau de conteneurs.</td>
                <td>Configuration d'un reverse proxy dans Nginx (<code>location /api/ { proxy_pass http://api:5000/api/; }</code>).</td>
                <td>Ne jamais exposer de noms DNS internes aux clients web : toujours passer par une passerelle inverse (Reverse Proxy).</td>
            </tr>
            <tr>
                <td><strong>ErrImagePull / ImagePullBackOff</strong> sur Minikube</td>
                <td>Kubernetes utilise par défaut le tag <code>latest</code> avec <code>imagePullPolicy: Always</code>, interrogeant Docker Hub qui ne possède pas nos images locales.</td>
                <td>Attribution de tags sémantiques stricts (<code>v1.0.0</code>), préchargement via <code>minikube image load</code> et politique <code>imagePullPolicy: Never</code>.</td>
                <td>En environnement de test local, forcer l'usage des images locales pour garantir l'indépendance réseau.</td>
            </tr>
            <tr>
                <td><strong>Crash en boucle de l'API</strong> au premier lancement sous Compose</td>
                <td>PostgreSQL met 4 à 5 secondes à exécuter les scripts de démarrage <code>init.sql</code>. L'API tentait une connexion immédiate sur un port non ouvert.</td>
                <td>Ajout d'une sonde de santé <code>pg_isready</code> sur PostgreSQL et clause <code>condition: service_healthy</code> dans <code>compose.yaml</code>.</td>
                <td>Un conteneur "démarré" n'est pas forcément "prêt" : toujours synchroniser sur l'état sain (healthy).</td>
            </tr>
            <tr>
                <td><strong>Redémarrages en cascade des Pods API</strong> lors d'une coupure base</td>
                <td>La connectivité à la base de données était initialement intégrée dans la sonde de vivacité (Liveness probe).</td>
                <td>Séparation stricte : la Liveness teste uniquement le process Express, la Readiness teste la liaison PostgreSQL.</td>
                <td>Ne jamais lier la vie d'un composant applicatif à la disponibilité de ses dépendances distantes.</td>
            </tr>
            <tr>
                <td><strong>Taille d'image frontend prohibitive (80+ Mo)</strong></td>
                <td>Le Dockerfile initial copiait le code source et lançait le serveur de développement Vite avec Node.js en production.</td>
                <td>Multi-Stage Build : compilation statique sous Node, puis transfert exclusif des fichiers <code>dist/</code> sous Nginx Alpine (5.56 Mo).</td>
                <td>Séparer hermétiquement l'environnement d'outillage de build et l'environnement d'exécution de production.</td>
            </tr>
            <tr>
                <td><strong>Port 3000 déjà utilisé sous Windows</strong></td>
                <td>Un conteneur précédent n'avait pas été arrêté proprement avant de relancer les tests.</td>
                <td>Création du script d'assainissement <code>scripts/cleanup.ps1</code> qui purge les conteneurs orphelins avant chaque exécution.</td>
                <td>Automatiser le nettoyage de l'infrastructure pour assurer des tests reproductibles et idempotents.</td>
            </tr>
            <tr>
                <td><strong>Erreur 400 lors de tests d'insertion</strong> avec des espaces seuls</td>
                <td>La validation backend vérifiait <code>if (title)</code>, ce qui laissait passer les chaînes composées uniquement d'espaces (<code>"   "</code>).</td>
                <td>Application systématique de <code>title.trim()</code> et validation de la longueur minimale et maximale dans <code>app.js</code>.</td>
                <td>Ne jamais faire confiance aux entrées utilisateurs : valider et assainir rigoureusement côté serveur.</td>
            </tr>
        </tbody>
    </table>

    <h3>Deux Extraits de Code : Avant / Après</h3>
    <p><strong>1. Correction du redémarrage en cascade dans les sondes Kubernetes :</strong></p>
    <pre><code>// AVANT (Problématique) : Sonde unique de vivacité vérifiant la base
app.get('/api/health', async (req, res) => {
  const dbOk = await db.testConnection();
  if (!dbOk) return res.status(500).send(); // Kubelet tue le Pod inutilement !
  res.status(200).send();
});

// APRÈS (Résolu dans application/backend/src/app.js) : Sondes découplées
app.get('/api/health/live', (req, res) => {
  res.status(200).json({ status: 'alive', uptime: process.uptime() }); // Process vivant ? Oui -> Ne pas tuer !
});
app.get('/api/health/ready', async (req, res) => {
  const dbOk = await db.testConnection();
  if (!dbOk) return res.status(503).json({ status: 'not_ready' }); // Base indisponible ? Retirer du pool de trafic !
  res.status(200).json({ status: 'ready' });
});</code></pre>
    """)
    
    # SECTION 9
    html_parts.append("""
    <div class="page-break"></div>
    <h2>9. Questions probables à la soutenance (18 Questions & Réponses percutantes)</h2>
    <p>Voici les questions techniques les plus fréquemment posées par les jurys lors des soutenances de projets de virtualisation et cloud. Apprenez à formuler ces réponses avec vos propres mots :</p>

    <div class="qa-card">
        <div class="qa-header">Q1 : Quelle est la différence fondamentale entre une Machine Virtuelle et un Conteneur Docker ?</div>
        <div class="qa-body">
            <p>Une <strong>Machine Virtuelle</strong> virtualise le matériel via un Hyperviseur (Type 1 ou Type 2). Chaque VM charge un système d'exploitation invité complet avec son propre noyau (kernel), ce qui consomme plusieurs gigaoctets et demande des minutes pour démarrer.</p>
            <p>Un <strong>Conteneur</strong> effectue une virtualisation au niveau du système d'exploitation : il partage directement le noyau Linux de la machine hôte. Il isole les processus grâce aux <strong>Namespaces</strong> (qui limitent ce que le processus peut <em>voir</em>) et aux <strong>cgroups</strong> (qui limitent ce que le processus peut <em>utiliser</em>). Un conteneur démarre en quelques millisecondes et ne pèse que quelques mégaoctets.</p>
            <span class="qa-cite">📁 Référence : Diapositives Conteneurisation (p. 4-6) & Virtualisation (p. 5-7).</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q2 : Pourquoi avoir utilisé un Reverse Proxy Nginx plutôt que d'exposer directement le port de l'API Node.js ?</div>
        <div class="qa-body">
            <p>Notre interface React s'exécute côté client dans le navigateur de l'utilisateur sur la machine hôte. L'hôte Windows ne peut pas résoudre les noms d'hôtes internes du réseau de conteneurs (<code>http://api:5000</code>). Nginx sert le site web et relaie en interne les requêtes <code>/api/*</code> vers le conteneur API. Cela garantit une communication <strong>Same-Origin</strong> (zéro erreur CORS) et permet de n'exposer qu'un seul port public (3000 ou 30080), laissant l'API et la base totalement privées.</p>
            <span class="qa-cite">📁 Référence : application/frontend/nginx.conf & ADR-001.</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q3 : Pourquoi avoir choisi un Déploiement avec PVC plutôt qu'un StatefulSet pour PostgreSQL ?</div>
        <div class="qa-body">
            <p>Dans notre projet, PostgreSQL est une instance unique autonome sans réplication ni cluster maître-esclave. Le <code>StatefulSet</code> est indispensable lorsqu'on gère des identités réseau ordinales et ordonnées (<code>postgres-0</code>, <code>postgres-1</code>). Pour une instance unique, un <strong>Deployment avec 1 réplica, un PVC et la stratégie Recreate</strong> offre la persistance requise tout en garantissant que l'ancien Pod libère le verrouillage du volume <code>ReadWriteOnce</code> avant que le nouveau ne le monte.</p>
            <span class="qa-cite">📁 Référence : kubernetes/04-database-deployment.yaml & ADR-002.</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q4 : Pourquoi découpler la sonde de vivacité (Liveness) de la sonde de préparation (Readiness) ?</div>
        <div class="qa-body">
            <p>La sonde <strong>Liveness</strong> (<code>/api/health/live</code>) surveille la santé du processus Node.js. Si elle échoue, Kubernetes redémarre le conteneur. La sonde <strong>Readiness</strong> (<code>/api/health/ready</code>) vérifie que la connexion PostgreSQL est active. Si la base de données est temporairement redémarrée, la Readiness échoue et Kubernetes retire le Pod du pool de routage sans le tuer. Si nous avions testé la base dans la Liveness, Kubernetes aurait tué et redémarré en boucle tous les Pods API, créant une tempête de reboots en cascade.</p>
            <span class="qa-cite">📁 Référence : application/backend/src/app.js (lignes 22-58) & kubernetes/06-api-deployment.yaml.</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q5 : Pourquoi configurer 'imagePullPolicy: Never' dans vos manifestes Kubernetes ?</div>
        <div class="qa-body">
            <p>En utilisant le tag <code>latest</code>, Kubernetes applique par défaut la politique <code>Always</code> et tente de télécharger l'image depuis Docker Hub, ce qui provoque une erreur <code>ImagePullBackOff</code> si les images ne sont pas publiées publiquement. En taguant nos images en <code>v1.0.0</code> et en définissant <code>imagePullPolicy: Never</code>, nous forçons Kubernetes à utiliser les images préchargées dans le cache de Minikube (via <code>minikube image load</code>), assurant une reproductibilité parfaite et autonome sans connexion Internet.</p>
            <span class="qa-cite">📁 Référence : kubernetes/06-api-deployment.yaml & ADR-003.</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q6 : Comment la segmentation réseau de Docker Compose protège-t-elle votre base de données ?</div>
        <div class="qa-body">
            <p>Dans <code>compose.yaml</code>, nous déclarons deux réseaux ponts : <code>frontend-net</code> et <code>backend-net</code>. Le conteneur <code>frontend</code> appartient uniquement à <code>frontend-net</code>, <code>postgres</code> uniquement à <code>backend-net</code>, et l'API <code>api</code> rejoint les deux. Parce que les ponts Docker isolent le trafic ARP et IP de niveau 2 et 3, le conteneur Nginx est techniquement incapable de joindre ou de pinger le port 5432 de la base de données.</p>
            <span class="qa-cite">📁 Référence : compose.yaml (lignes 81-90) & ADR-004.</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q7 : Un Namespace Kubernetes fournit-il une isolation de sécurité réseau par défaut ?</div>
        <div class="qa-body">
            <p><strong>Non.</strong> Un Namespace Kubernetes est une frontière <em>administrative et logique</em> (il permet d'attribuer des quotas de ressources et d'éviter les collisions de noms entre équipes). Par défaut, le réseau Kubernetes est totalement plat : n'importe quel Pod d'un autre namespace peut envoyer des paquets IP à nos Pods. Pour obtenir une véritable isolation réseau dans Kubernetes, il faut déclarer des ressources <code>NetworkPolicy</code> avec un plugin CNI compatible (comme Calico ou Cilium).</p>
            <span class="qa-cite">📁 Référence : Diapositives Conteneurisation (p. 44) & README.md.</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q8 : Comment avez-vous obtenu une réduction de 93.1% sur la taille de l'image Frontend ?</div>
        <div class="qa-body">
            <p>Grâce au <strong>Multi-Stage Build</strong>. Dans une image standard à un seul étage, l'image finale embarque le runtime Node.js, le gestionnaire npm, les modules node_modules et le code source (80.92 MB). Notre Dockerfile sépare la construction en deux étages : l'étape <code>builder</code> compile les sources en HTML/CSS/JS pur dans le dossier <code>dist/</code>, puis l'étape <code>runner</code> copie uniquement ce dossier dans <code>nginx:stable-alpine-slim</code>. Tout l'outillage de compilation est jeté, produisant une image finale de seulement <strong>5.56 MB</strong>.</p>
            <span class="qa-cite">📁 Référence : application/frontend/Dockerfile & docs/benchmarks/image-sizes.md.</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q9 : Que se passe-t-il si un Pod API plante ou est supprimé brutalement en production ?</div>
        <div class="qa-body">
            <p>Le contrôleur <strong>ReplicaSet</strong> de Kubernetes applique la boucle de réconciliation continue : il compare l'état désiré (déclaré dans le Deployment, ex: 2 réplicas) avec l'état réel du cluster. Dès que le Pod disparaît, le ReplicaSet instancie immédiatement un Pod de remplacement, le <strong>Scheduler</strong> l'affecte à un nœud disponible, et le <strong>Kubelet</strong> démarre le conteneur. Dès que la sonde Readiness est validée, le Pod est réintégré au Service. Le client ne subit aucune interruption de service.</p>
            <span class="qa-cite">📁 Référence : kubernetes/06-api-deployment.yaml & Test T09.</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q10 : Comment vos données PostgreSQL survivent-elles à la destruction de son Pod ?</div>
        <div class="qa-body">
            <p>Le Pod monte un <strong>PersistentVolumeClaim</strong> (<code>03-database-pvc.yaml</code>) de 1Gi. Ce PVC est lié à un volume persistant physique managé par la StorageClass de Minikube. Lorsque le Pod PostgreSQL est détruit, le cycle de vie du volume persistant reste indépendant du Pod. Le nouveau Pod instancié par le Deployment ré-attache le même volume et retrouve immédiatement les tables et les données existantes.</p>
            <span class="qa-cite">📁 Référence : kubernetes/03-database-pvc.yaml & Test T10.</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q11 : Comment se fait la découverte de service (Service Discovery) dans Kubernetes ?</div>
        <div class="qa-body">
            <p>Dans Kubernetes, les Pods ont des adresses IP dynamiques qui changent à chaque recréation. Pour les stabiliser, on associe aux Pods un <strong>Service</strong> (ex: <code>service/api</code>). Kubernetes lui attribue une adresse IP virtuelle fixe (ClusterIP) et enregistre son nom dans le serveur DNS interne du cluster (<strong>CoreDNS</strong>). Les autres conteneurs peuvent alors simplement contacter <code>http://api:5000</code>. Le composant <strong>kube-proxy</strong> intercepte ces requêtes et les redirige vers les adresses IP réelles des Pods sains.</p>
            <span class="qa-cite">📁 Référence : kubernetes/07-api-service.yaml & Diapositives Conteneurisation (p. 45).</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q12 : Quelle est la différence entre un Service ClusterIP et un Service NodePort ?</div>
        <div class="qa-body">
            <p>Un Service <strong>ClusterIP</strong> est le type par défaut : il n'est accessible que <em>depuis l'intérieur du cluster</em> via une adresse IP virtuelle privée (utilisé pour notre API et notre base). Un Service <strong>NodePort</strong> ouvre un port statique dédié (compris entre 30000 et 32767) sur toutes les interfaces réseau de chaque nœud du cluster, permettant à des clients externes d'accéder au service (utilisé sur le port 30080 pour notre Frontend).</p>
            <span class="qa-cite">📁 Référence : kubernetes/05-database-service.yaml & kubernetes/09-frontend-service.yaml.</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q13 : Comment fonctionne le contrôle des ressources via les cgroups dans vos manifestes ?</div>
        <div class="qa-body">
            <p>Dans <code>06-api-deployment.yaml</code>, nous déclarons <code>requests</code> (ressources garanties réservées par le Scheduler pour placer le Pod) et <code>limits</code> (plafond maximal autorisé). Pour la mémoire (256Mi), si le conteneur dépasse la limite, le noyau Linux déclenche l'Out-Of-Memory Killer (OOM-Kill) et redémarre le conteneur. Pour le CPU (250m = 0.25 cœur), le noyau Linux utilise le Completely Fair Scheduler (CFS) pour brider les cycles processeur sans tuer le processus.</p>
            <span class="qa-cite">📁 Référence : Diapositives Conteneurisation (p. 11) & kubernetes/06-api-deployment.yaml.</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q14 : Pourquoi exécuter l'API Node.js avec 'USER node' plutôt qu'en utilisateur par défaut ?</div>
        <div class="qa-body">
            <p>Par défaut, Docker exécute les conteneurs avec l'UID 0 (<code>root</code>). Si une faille dans une dépendance npm permet à un attaquant d'exécuter des commandes à distance, il dispose des privilèges administrateur à l'intérieur du conteneur et peut exploiter une vulnérabilité du noyau pour s'échapper sur l'hôte. Avec <code>USER node</code>, le processus tourne avec un compte applicatif restreint, respectant le principe du moindre privilège.</p>
            <span class="qa-cite">📁 Référence : application/backend/Dockerfile (ligne 22).</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q15 : Comment les secrets sont-ils gérés entre votre démo et un environnement de production ?</div>
        <div class="qa-body">
            <p>Dans notre projet académique, nous découplons la configuration dans un <code>ConfigMap</code> et les identifiants dans un <code>Secret</code> natif (<code>02-api-secret.yaml</code>). Cependant, les Secrets natifs de Kubernetes ne sont que de simples chaînes encodées en Base64. En production sur AWS, nous utiliserions <strong>AWS Secrets Manager</strong> avec chiffrement d'enveloppe via <strong>AWS KMS</strong>, synchronisé dans le cluster via l'<strong>External Secrets Operator (ESO)</strong> avec rotation automatique des mots de passe.</p>
            <span class="qa-cite">📁 Référence : kubernetes/02-api-secret.yaml & docs/aws-comparison.md.</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q16 : En quoi l'étude de cas Wikileaks du cours de Cloud s'applique-t-elle à ContainerLab ?</div>
        <div class="qa-body">
            <p>En 2010, Wikileaks a subi une attaque DDoS géante (>10 Gbps) puis une rupture brutale de contrat par Amazon AWS. Cela nous apprend que la résilience repose sur deux piliers : l'<strong>élasticité</strong> (pouvoir multiplier les réplicas face à une charge soudaine, comme nous le faisons avec <code>kubectl scale</code>) et la <strong>portabilité sans vendor lock-in</strong> (nos conteneurs peuvent être redéployés à l'identique sur n'importe quel cloud ou sur site en une commande).</p>
            <span class="qa-cite">📁 Référence : Diapositives Cloud Computing (p. 40-47).</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q17 : Comment votre projet serait-il déployé sur AWS en environnement de production ?</div>
        <div class="qa-body">
            <p>Sur AWS :</p>
            <ul>
                <li>Le cluster Minikube deviendrait un cluster managé <strong>Amazon EKS</strong> avec nœuds managés multi-AZ.</li>
                <li>Le service NodePort serait remplacé par un <strong>Application Load Balancer (ALB)</strong> avec certificat SSL et protection AWS WAF.</li>
                <li>Les images locales seraient stockées sur <strong>Amazon ECR</strong> avec scan de vulnérabilités CVE.</li>
                <li>La base de données PostgreSQL conteneurisée serait remplacée par une instance managée <strong>Amazon RDS PostgreSQL Multi-AZ</strong> avec basculement automatique et sauvegardes continues.</li>
            </ul>
            <span class="qa-cite">📁 Référence : docs/aws-comparison.md.</span>
        </div>
    </div>

    <div class="qa-card">
        <div class="qa-header">Q18 : Quel est l'équivalent de votre architecture sous Amazon ECS et AWS Fargate ?</div>
        <div class="qa-body">
            <p>Dans <strong>Amazon ECS</strong>, le Pod Kubernetes correspond à une <strong>Task Definition</strong> (qui déclare les images de conteneurs, le CPU et la RAM). Le Deployment Kubernetes correspond à un <strong>ECS Service</strong> (qui maintient le nombre de tâches désiré). En mode <strong>AWS Fargate</strong>, nous n'avons aucune machine virtuelle EC2 à gérer : AWS gère le serveur et le noyau, et facture uniquement le CPU et la mémoire consommés par tâche à la seconde.</p>
            <span class="qa-cite">📁 Référence : README.md (Section 11) & docs/aws-comparison.md (Section 5).</span>
        </div>
    </div>
    """)
    
    # SECTION 10
    html_parts.append("""
    <div class="page-break"></div>
    <h2>10. Le grand glossaire en une phrase</h2>
    <p>Chaque terme technique expliqué en une phrase simple et limpide avec sa correspondance directe dans ContainerLab :</p>

    <table>
        <thead>
            <tr>
                <th style="width: 20%;">Terme Technique</th>
                <th style="width: 55%;">Définition en une phrase</th>
                <th style="width: 25%;">Localisation dans le Projet</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Hyperviseur</strong></td>
                <td>Logiciel (Type 1 bare-metal ou Type 2 hosted) qui émule du matériel pour exécuter des machines virtuelles complètes avec leur propre OS invité.</td>
                <td>Cours Virtualisation (p. 6-7)</td>
            </tr>
            <tr>
                <td><strong>chroot</strong></td>
                <td>Appel système Unix (1979) qui modifie le répertoire racine d'un processus, précurseur de l'isolation du système de fichiers des conteneurs.</td>
                <td>Cours Conteneurisation (p. 10)</td>
            </tr>
            <tr>
                <td><strong>Control Groups (cgroups)</strong></td>
                <td>Mécanisme du noyau Linux (2006) qui bride et surveille la consommation des ressources physiques (CPU, RAM, disques I/O).</td>
                <td><code>06-api-deployment.yaml</code></td>
            </tr>
            <tr>
                <td><strong>Namespaces</strong></td>
                <td>Fonctionnalité du noyau Linux (2008) qui partitionne les ressources globales pour donner à chaque conteneur sa propre vue isolée (PID, réseau, montages).</td>
                <td>Noyau Linux hôte (Docker/K8s)</td>
            </tr>
            <tr>
                <td><strong>OverlayFS</strong></td>
                <td>Système de fichiers empilant des couches immuables en lecture seule sous une fine couche supérieure inscriptible en Copy-on-Write (CoW).</td>
                <td>Moteur de stockage Docker</td>
            </tr>
            <tr>
                <td><strong>Multi-Stage Build</strong></td>
                <td>Technique Dockerfile qui sépare l'étape de compilation logicielle de l'étape d'exécution finale pour minimiser la taille et sécuriser l'image.</td>
                <td><code>application/frontend/Dockerfile</code></td>
            </tr>
            <tr>
                <td><strong>Docker Compose</strong></td>
                <td>Outil d'orchestration locale permettant de déclarer et démarrer plusieurs conteneurs interconnectés via un fichier YAML unique.</td>
                <td><code>compose.yaml</code></td>
            </tr>
            <tr>
                <td><strong>Zone Démilitarisée (DMZ)</strong></td>
                <td>Sous-réseau intermédiaire isolant les serveurs exposés à Internet des systèmes internes critiques et des bases de données.</td>
                <td><code>frontend-net</code> / <code>backend-net</code></td>
            </tr>
            <tr>
                <td><strong>Pod</strong></td>
                <td>La plus petite unité déployable et orchestrable dans Kubernetes, regroupant un ou plusieurs conteneurs partageant la même IP et le même stockage.</td>
                <td>Objets Pods du cluster</td>
            </tr>
            <tr>
                <td><strong>ReplicaSet</strong></td>
                <td>Contrôleur Kubernetes dont l'unique mission est de garantir qu'un nombre précis de réplicas identiques d'un Pod sont en cours d'exécution.</td>
                <td>Géré par les <code>Deployments</code></td>
            </tr>
            <tr>
                <td><strong>Deployment</strong></td>
                <td>Objet déclaratif Kubernetes de niveau supérieur qui supervise les ReplicaSets et permet les montées de version (rollout) sans interruption.</td>
                <td><code>06-api-deployment.yaml</code></td>
            </tr>
            <tr>
                <td><strong>Service ClusterIP</strong></td>
                <td>Service Kubernetes interne fournissant une adresse IP virtuelle stable et un nom DNS pour équilibrer le trafic au sein du cluster.</td>
                <td><code>05-database-service.yaml</code></td>
            </tr>
            <tr>
                <td><strong>Service NodePort</strong></td>
                <td>Service Kubernetes exposant une application à l'extérieur du cluster via un port statique dédié sur tous les nœuds de calcul.</td>
                <td><code>09-frontend-service.yaml</code></td>
            </tr>
            <tr>
                <td><strong>kube-proxy</strong></td>
                <td>Composant réseau exécuté sur chaque nœud Kubernetes qui traduit les IPs virtuelles des Services en règles de filtrage de paquets iptables.</td>
                <td>Nœud Minikube</td>
            </tr>
            <tr>
                <td><strong>PersistentVolumeClaim (PVC)</strong></td>
                <td>Demande formelle de stockage persistant formulée par un Pod sans avoir à connaître l'infrastructure physique sous-jacente.</td>
                <td><code>03-database-pvc.yaml</code></td>
            </tr>
            <tr>
                <td><strong>StorageClass</strong></td>
                <td>Fournisseur de stockage Kubernetes permettant d'allouer dynamiquement des volumes physiques (HostPath sur Minikube, EBS sur AWS).</td>
                <td><code>standard</code> (Minikube)</td>
            </tr>
            <tr>
                <td><strong>Liveness Probe</strong></td>
                <td>Sonde de vivacité périodique vérifiant si le processus applicatif est toujours vivant, sous peine d'être redémarré par le kubelet.</td>
                <td><code>GET /api/health/live</code></td>
            </tr>
            <tr>
                <td><strong>Readiness Probe</strong></td>
                <td>Sonde de préparation vérifiant si le conteneur est apte à recevoir du trafic client, sous peine d'être retiré temporairement du Service.</td>
                <td><code>GET /api/health/ready</code></td>
            </tr>
            <tr>
                <td><strong>ConfigMap</strong></td>
                <td>Objet Kubernetes stockant des paires clé-valeur de configuration non sensibles, injectées dans les conteneurs sous forme de variables d'environnement.</td>
                <td><code>01-configmap.yaml</code></td>
            </tr>
            <tr>
                <td><strong>Secret</strong></td>
                <td>Objet Kubernetes contenant des données sensibles (mots de passe, clés d'API) encodées en base64 pour découpler la sécurité du code source.</td>
                <td><code>02-api-secret.yaml</code></td>
            </tr>
            <tr>
                <td><strong>Self-Healing (Auto-Guérison)</strong></td>
                <td>Capacité d'un orchestrateur à détecter la disparition d'un conteneur défaillant et à recréer automatiquement une instance saine.</td>
                <td>Test T09</td>
            </tr>
            <tr>
                <td><strong>Minikube</strong></td>
                <td>Distribution légère de Kubernetes exécutant un cluster à nœud unique dans un conteneur Docker pour le développement et l'évaluation locale.</td>
                <td>Environnement de test principal</td>
            </tr>
            <tr>
                <td><strong>IaaS (Infrastructure as a Service)</strong></td>
                <td>Modèle de cloud fournissant des ressources matérielles virtualisées fondamentales (serveurs EC2, disques EBS, réseaux VPC).</td>
                <td>Cours Cloud Computing (p. 50)</td>
            </tr>
            <tr>
                <td><strong>PaaS (Platform as a Service)</strong></td>
                <td>Modèle de cloud fournissant un environnement prêt à l'emploi pour exécuter et déployer du code sans administrer les serveurs.</td>
                <td>Cours Cloud Computing (p. 56)</td>
            </tr>
            <tr>
                <td><strong>SaaS (Software as a Service)</strong></td>
                <td>Modèle de cloud délivrant une application logicielle complète accessible par navigateur web sans aucune installation locale.</td>
                <td>Cours Cloud Computing (p. 61)</td>
            </tr>
            <tr>
                <td><strong>Amazon EKS</strong></td>
                <td>Service managé AWS qui déploie et administre le Control Plane de Kubernetes de manière hautement disponible sur 3 zones de disponibilité.</td>
                <td>Projection Cloud (Section 11)</td>
            </tr>
            <tr>
                <td><strong>Amazon ECS</strong></td>
                <td>Orchestrateur de conteneurs natif d'Amazon Web Services, plus simple que Kubernetes et profondément intégré aux services AWS.</td>
                <td>README.md & docs/aws-comparison</td>
            </tr>
            <tr>
                <td><strong>AWS Fargate</strong></td>
                <td>Moteur de calcul serverless pour conteneurs permettant d'exécuter des tâches ECS ou Pods EKS sans provisionner de serveurs EC2.</td>
                <td>docs/aws-comparison.md</td>
            </tr>
            <tr>
                <td><strong>Application Load Balancer (ALB)</strong></td>
                <td>Équilibreur de charge de niveau 7 (HTTP/HTTPS) chez AWS assurant le routage basé sur les chemins d'URL et la terminaison SSL.</td>
                <td>docs/aws-comparison.md</td>
            </tr>
            <tr>
                <td><strong>Amazon RDS</strong></td>
                <td>Service de base de données relationnelle managée chez AWS assurant les sauvegardes automatiques, les correctifs et le basculement Multi-AZ.</td>
                <td>docs/aws-comparison.md</td>
            </tr>
            <tr>
                <td><strong>Amazon ECR</strong></td>
                <td>Registre de conteneurs Docker privé et sécurisé chez AWS avec analyse automatique des vulnérabilités de sécurité.</td>
                <td>docs/aws-comparison.md</td>
            </tr>
            <tr>
                <td><strong>Vendor Lock-in</strong></td>
                <td>Situation de dépendance captive où un client ne peut pas quitter un fournisseur de cloud sans coûts et réécritures prohibitifs.</td>
                <td>Étude de cas Wikileaks</td>
            </tr>
        </tbody>
    </table>
    """)
    
    # SECTION 11
    html_parts.append("""
    <div class="page-break"></div>
    <h2>11. Checklist avant la soutenance & conseils pour le jour J</h2>

    <h3>La Veille au Soir</h3>
    <ul>
        <li>[ ] Vérifier que <code>git status</code> est totalement propre (zéro modification non validée).</li>
        <li>[ ] Lancer <code>.\\scripts\\run-tests.ps1 -Target compose</code> pour confirmer que les tests locaux passent tous avec succès.</li>
        <li>[ ] Recharger la batterie du PC portable à 100% et glisser le chargeur secteur dans le sac.</li>
        <li>[ ] Relire les 18 questions de la Section 9 avec son binôme et répondre à voix haute.</li>
    </ul>

    <h3>15 Minutes Avant le Passage</h3>
    <ul>
        <li>[ ] Fermer toutes les applications inutiles (messageries, onglets superflus) pour libérer la RAM.</li>
        <li>[ ] Lancer Docker Desktop et exécuter <code>minikube start --driver=docker</code>.</li>
        <li>[ ] Précharger les images : <code>.\\scripts\\load-images.ps1</code>.</li>
        <li>[ ] Déployer les manifestes : <code>.\\scripts\\deploy-k8s.ps1</code>.</li>
        <li>[ ] Ouvrir deux fenêtres terminal : l'une pour taper les commandes, l'autre avec <code>kubectl get pods -n containerlab -w</code>.</li>
        <li>[ ] Ouvrir le navigateur sur le tableau de bord web et tester un clic sur <em>"Send 6 Calls"</em> pour valider que tout est vert.</li>
    </ul>

    <h3>Pendant la Soutenance</h3>
    <ul>
        <li>[ ] <strong>Alterner la parole de façon équilibrée :</strong> Montrez au jury que vous formez un binôme soudé et que chacun comprend l'ensemble du projet.</li>
        <li>[ ] <strong>Montrer du code et des commandes :</strong> Ne restez jamais bloqués sur des diapositives théoriques. Ouvrez les Dockerfiles, le fichier <code>compose.yaml</code> et les manifestes Kubernetes pour prouver chaque affirmation technique.</li>
        <li>[ ] <strong>Mettre en valeur les chiffres clés :</strong> Citez spontanément la réduction de <strong>93.1%</strong> sur l'image Frontend et les <strong>11 tests T01 à T11</strong> automatisés.</li>
        <li>[ ] <strong>Si l'on ne sait pas répondre :</strong> Ne jamais inventer. Dites avec assurance : <em>"Nous n'avons pas rencontré ce cas spécifique, mais voici comment nous le vérifierions dans le fichier de configuration..."</em> puis montrez le code. Les jurys apprécient l'honnêteté et la démarche d'ingénieur.</li>
    </ul>

    <div class="callout callout-success" style="margin-top: 25px; text-align: center; padding: 16px;">
        <div style="font-size: 13pt; font-weight: 800; margin-bottom: 5px; color: #166534;">🎓 Bonne chance à Houssem et Nour pour votre soutenance !</div>
        <div style="font-size: 9.5pt; color: #15803d;">Vous avez construit un projet d'une qualité technique irréprochable, parfaitement aligné avec le cours et le barème. Présentez-le avec fierté et sérénité.</div>
    </div>
    """)
    
    html_parts.append("</body></html>")
    
    full_html = "".join(html_parts)
    
    html_path = os.path.join(base_dir, "docs", "guide-apprentissage-soutenance.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"HTML guide generated at: {html_path} ({len(full_html)} chars)")
    
    # Write full Markdown document
    md_content = """# ContainerLab — Guide d’Apprentissage, de Démo et de Soutenance
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
"""
    
    md_path = os.path.join(base_dir, "docs", "guide-apprentissage-soutenance.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Full Markdown guide written at: {md_path}")
    
    # Compile to PDF using Microsoft Edge headless
    desktop_pdf = r"C:\Users\houss\Desktop\ContainerLab_Guide_Apprentissage_Soutenance.pdf"
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_exe):
        edge_exe = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        
    print(f"Rendering PDF with Edge headless to: {desktop_pdf}...")
    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={desktop_pdf}",
        html_path
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(desktop_pdf):
        size = os.path.getsize(desktop_pdf)
        print(f"SUCCESS! PDF successfully compiled: {desktop_pdf} ({size} bytes)")
    else:
        print(f"Edge execution finished with code {res.returncode}. Output: {res.stdout} Err: {res.stderr}")

if __name__ == "__main__":
    main()
