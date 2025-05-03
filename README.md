# AlloMédecin - Plateforme de Téléconsultation Médicale

Bienvenue sur le projet **AlloMédecin**, une plateforme de téléconsultation permettant aux patients de réserver des rendez-vous avec des médecins, de consulter à distance et de gérer leur dossier médical.

---

## 🚀 Objectif du projet

Offrir une solution complète, sécurisée et accessible, adaptée aux réalités africaines (connexion lente, besoin d’accompagnement), pour faciliter l'accès aux soins médicaux à distance.

---

## 🔧 Stack Technique (Phase 1)

- **Backend** : Django REST Framework
- **Base de données** : PostgreSQL
- **Authentification** : JWT
- **Frontend** (prochaine phase) : React.js
- **Outils** : Git, GitHub, Postman, Docker (plus tard)

---

## 👥 Équipe

Team Spark (MIABE HACKATON)

---

## 📦 Fonctionnalités ciblées pour la démo initiale (Phase 1)

1. **Gestion des utilisateurs**
   - Inscription / Connexion
   - Séparation rôles (Patient / Médecin / Admin)
   - JWT Authentication
   - Mise à jour du profil

2. **Gestion des rendez-vous**
   - CRUD des rendez-vous
   - Planning des disponibilités médecins

3. **Consultation (bêta)**
   - Démarrage du module de consultation vidéo (mock WebRTC)

4. **Dossier Médical (début)**
   - Ajout de documents médicaux au profil

---


## 📁 Structure du Projet (exemple)

```bash
allomedecin/
│
├── users/               # Gestion des utilisateurs
├── rdv/                 # Rendez-vous
├── dossier/             # Dossier Médical
├── settings/            # Configuration Django
├── manage.py
└── README.md
```

---

## 🧾 Règles de collaboration

1. **Travail en branches**
   - Ne pas coder directement sur `main`
   - Créer une branche par fonctionnalité : `feature/nom_fonction`
   - Exemple : `feature/authentication`

2. **Commits propres et explicites**
   - Exemples :
     - ✅ `add authentication logic with JWT`
     - 🐛 `fix bug on rendezvous filtering`
     - 🎨 `refactor dossier models`

3. **Pull Request obligatoire**
   - Toujours ouvrir une PR vers `main`
   - Ajouter une description claire de ce que fait la PR

4. **Revue de code**
   - L’autre développeur valide la PR
   - On ne merge pas sa propre PR (sauf cas d’urgence)

5. **Tests**
   - Chaque nouvelle fonctionnalité doit avoir au minimum un test

6. **Respect de la sécurité**
   - Jamais de credentials ou secret keys dans le code
   - `.env` pour toutes les variables sensibles (non versionné)

---

## 🧪 Comment démarrer en local

```bash
# Clone le projet
git clone https://github.com/ton-compte/allomedecin.git
cd allomedecin

# Crée ton environnement virtuel
python -m venv env
source env/bin/activate  # Windows : env\Scripts\activate

# Installe les dépendances
pip install -r requirements.txt

# Crée la base de données
python manage.py makemigrations
python manage.py migrate

# Crée un superuser
python manage.py createsuperuser

# Lance le serveur
python manage.py runserver
```

---

## 🛡️ Sécurité & Conformité

- Données sensibles chiffrées
- Logs des accès
- Conformité RGPD Bénin
- Anonymisation des données pour les stats

---

## 📌 Prochaine Phase (Frontend)

- Interface en React.js
- Authentification JWT avec axios interceptors
- Interface patients + médecins
- Vidéo (WebRTC ou Jitsi)
- Notifications push (FCM)

---

