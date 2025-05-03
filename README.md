
# 🩺 AlloMédecin – Plateforme de mise en relation médecins/patients

Ce projet collaboratif vise à développer une API robuste permettant aux patients de consulter des médecins, de prendre rendez-vous, et plus encore.

---

## 🚀 Technologies utilisées

- Django>=4.2
- djangorestframework
- djangorestframework-simplejwt
- psycopg2-binary
- python-dotenv
- drf-yasg (Swagger et ReDoc pour la documentation)

---

## ⚙️ Mise en route

1. Cloner le projet :
   ```bash
   git clone https://github.com/ton-utilisateur/AlloMedecin.git
   cd AlloMedecin
````

2. Créer un environnement virtuel :

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Installer les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

4. Configurer la base de données dans `.env` :

   ```
   DB_NAME=...
   DB_USER=...
   DB_PASSWORD=...
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. Appliquer les migrations :

   ```bash
   python manage.py migrate
   ```

---

## 🧠 Stratégie Git

* `main` : branche **stable**, protégée. Aucune modification directe ne doit être faite ici.
* `develop` : branche de développement.
* `feature/*` : pour toute nouvelle fonctionnalité.
* `fix/*` : pour les correctifs.
* `hotfix/*` : correctif urgent à appliquer sur `main`.

---

## ✅ Règles de contribution

* ⚠️ **Ne jamais pousser directement sur `main`.**
* Créer une branche à partir de `develop` :

  ```bash
  git checkout develop
  git checkout -b feature/nom-fonction
  ```
* Commits clairs et significatifs.
* Ouvrir une **pull request vers `develop`** une fois votre travail terminé.
* Minimum **1 review obligatoire** avant merge.
* S'assurer que les tests passent et que la documentation (Swagger/ReDoc) est à jour.
* Rebaser votre branche régulièrement pour éviter les conflits.

---

## 📄 Documentation API

Une fois le projet lancé, la documentation sera accessible à :

* Swagger : `/swagger/`
* ReDoc : `/redoc/`

---

## 👥 Équipe de développement

Team Spark (MIABE HACKATON)
---

