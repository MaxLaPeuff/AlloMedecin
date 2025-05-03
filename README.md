
# 🩺 AlloMédecin – Plateforme de mise en relation médecins/patients

## Description

Le projet AlloMedecin est une application permettant de gérer les informations médicales et les consultations. Ce projet est développé avec Django et utilise PostgreSQL comme base de données.

## Prérequis

Avant de commencer, assurez-vous que vous avez installé les outils suivants :

- Python 3.12+ : [Télécharger Python](https://www.python.org/downloads/)
- PostgreSQL : [Télécharger PostgreSQL](https://www.postgresql.org/download/)
- Git : [Télécharger Git](https://git-scm.com/downloads)

## Installation

1. Clonez ce repository sur votre machine locale :

   ```bash
   git clone https://github.com/username/AlloMedecin.git
````

2. Allez dans le dossier du projet :

   ```bash
   cd AlloMedecin
   ```

3. Créez un environnement virtuel pour installer les dépendances :

   ```bash
   python3 -m venv venv
   ```

4. Activez l'environnement virtuel :

   * Sur macOS/Linux :

     ```bash
     source venv/bin/activate
     ```

   * Sur Windows :

     ```bash
     venv\Scripts\activate
     ```

5. Installez les dépendances à partir du fichier `requirements.txt` :

   ```bash
   pip install -r requirements.txt
   ```

6. **Configurer votre base de données PostgreSQL :**

   * Assurez-vous d'avoir PostgreSQL installé sur votre machine.
   * Créez une base de données PostgreSQL sur votre machine.

     ```bash
     CREATE DATABASE allomedecin;
     ```

7. **Configuration des variables d'environnement :**

   * Copiez le fichier `.env.example` en `.env` :

     ```bash
     cp .env.example .env
     ```

   * Ouvrez le fichier `.env` et modifiez les paramètres pour correspondre à vos informations locales de connexion à PostgreSQL et autres variables spécifiques à votre environnement :

     ```env
     # Variables de connexion à la base de données PostgreSQL
     DB_NAME=allomedecin
     DB_USER=your_db_user
     DB_PASSWORD=your_db_password
     DB_HOST=localhost
     DB_PORT=5432

     # Django secret key (à modifier sur chaque machine)
     SECRET_KEY=your_secret_key

     DEBUG=True
     ALLOWED_HOSTS=127.0.0.1, localhost
     ```

     **Explications des variables d'environnement :**

     * **DB\_NAME** : Le nom de la base de données PostgreSQL.
     * **DB\_USER** : L'utilisateur de la base de données (créez un utilisateur pour PostgreSQL si nécessaire).
     * **DB\_PASSWORD** : Le mot de passe de l'utilisateur de la base de données.
     * **DB\_HOST** : L'adresse de la machine PostgreSQL (en local pour vous).
     * **DB\_PORT** : Le port d'écoute de PostgreSQL (par défaut `5432`).
     * **SECRET\_KEY** : La clé secrète de Django, elle doit être unique et sécurisée sur chaque machine.
     * **DEBUG** : Indique si Django doit être en mode debug (utilisé pendant le développement).
     * **ALLOWED\_HOSTS** : Liste des hôtes autorisés pour le serveur Django, généralement `127.0.0.1` et `localhost`.

8. **Effectuer les migrations de base de données :**

   ```bash
   python3 manage.py migrate
   ```

9. **Démarrer le serveur Django en mode développement :**

   ```bash
   python3 manage.py runserver
   ```

   Vous pouvez maintenant accéder à l'application à l'adresse [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Règles de collaboration

### 1. Branches

Le workflow de développement se base sur un système de branches. Voici les principales règles :

* **`main`** : Branche principale contenant la version stable de l'application. Ne travaillez jamais directement sur cette branche.
* **`develop`** : Branche de développement contenant les dernières fonctionnalités en développement. Cette branche est à fusionner régulièrement avec `main` une fois les fonctionnalités terminées.
* **`feature/nom-fonctionnalite`** : Créez une branche pour chaque nouvelle fonctionnalité que vous développez. Nom de la branche : `feature/<nom_fonctionnalite>`. Ex : `feature/authentification`.

### 2. Protéger la branche `main`

La branche `main` est protégée. Seuls les commits validés via une Pull Request seront fusionnés.

### 3. Pull Requests (PR)

Lorsque vous avez terminé une fonctionnalité ou un bug, ouvrez une Pull Request pour fusionner votre branche de fonctionnalité avec `develop`. Une revue de code sera effectuée avant toute fusion.

### 4. Conventions de nommage des branches

* Utilisez des noms clairs et explicites pour les branches (par ex. `feature/login`, `bugfix/correction-auth`).

### 5. Mise à jour de votre branche

Avant de commencer à travailler sur une nouvelle fonctionnalité ou un correctif, assurez-vous que votre branche locale est à jour avec `develop` :

```bash
git checkout develop
git pull origin develop
git checkout <votre-branche>
git merge develop
```

### 6. Commits et messages

* Les messages de commit doivent être clairs et explicites.
* Utilisez le format suivant pour les messages de commit :

  * **`feature:`** Ajout d'une nouvelle fonctionnalité.
  * **`bugfix:`** Correction d'un bug.
  * **`docs:`** Modifications dans la documentation.
  * **`style:`** Modifications de style (espaces, indentation, etc.).
  * **`refactor:`** Refactorisation du code.

### 7. Environnement de développement

Chacun des développeurs doit configurer son propre environnement local. Assurez-vous que les variables d'environnement dans le fichier `.env` soient bien configurées avant de lancer l'application.

