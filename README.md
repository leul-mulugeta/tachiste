# 📝 Tachiste

## 🛠️ Présentation
Tachiste est une application web de gestionnaire de tâches (To-Do List) multi-utilisateurs et sécurisée. Développée avec le framework **Flask (Python)**, elle utilise **SQLAlchemy** pour assurer la persistance des données.

## 🚀 Fonctionnalités
- **Authentification Sécurisée** : Système complet d'inscription, connexion et déconnexion.
- **Hachage de Mots de Passe** : Les mots de passe des utilisateurs sont stockés de manière sécurisée grâce au hachage (via `Werkzeug`).
- **Base de Données Persistante** : Les utilisateurs et les tâches sont sauvegardés dans une base de données `SQLite`, gérée par l'ORM `SQLAlchemy`.
- **Architecture Multi-Utilisateurs** : Architecture sécurisée où **chaque utilisateur ne peut voir et modifier que ses propres tâches**.
- **Gestion Complète des Tâches** :
    - Ajouter une nouvelle tâche.
    - Supprimer une tâche.
    - Marquer une tâche comme "terminée" (ou l'annuler).
    - Marquer une tâche comme "importante".
- **Planification** : Possibilité d'ajouter une date et une heure d'échéance aux tâches.
- **Vues Filtrées** : L'interface est organisée en plusieurs vues pour une meilleure productivité :
    - **Mon Jour** : Affiche les tâches prévues pour aujourd'hui.
    - **Important** : Affiche toutes les tâches marquées comme importantes.
    - **Tâches** : Affiche toutes les tâches non terminées.
    - **Fini** : Affiche toutes les tâches terminées.

## 💻 Stack Technique
- **Backend** : **Python 3** avec **Flask** (micro-framework web).
- **Base de Données** : **SQLAlchemy** (ORM) connectée à **SQLite**.
- **Authentification** : **Flask-Login** (gestion des sessions) & **Werkzeug** (hachage).
- **Frontend** : **HTML5**, **CSS3** et moteur de templates **Jinja2**.

## ⚙️ Installation et Exécution

Avant de commencer, assurez-vous d'avoir **Python 3** et **pip** installés sur votre machine.

1.  **Clonez le dépôt** (ou téléchargez les fichiers) :
    ```sh
    git clone https://github.com/leul-mulugeta/tachiste.git
    cd tachiste
    ```

2.  **Créez un environnement virtuel** (recommandé) :
    ```sh
    python -m venv .venv
    ```

3.  **Activez l'environnement virtuel** :
    * Sur Windows :
        ```sh
        .venv\Scripts\activate
        ```
    * Sur macOS/Linux :
        ```sh
        source .venv/bin/activate
        ```

4.  **Installez les dépendances** listées dans `requirements.txt` :
    ```sh
    pip install -r requirements.txt
    ```

5.  **Lancez l'application** :
    ```sh
    python views.py
    ```
    L'application sera accessible à l'adresse `http://127.0.0.1:5000` dans votre navigateur.

## 🧑‍💻 À propos

Projet NSI initialement développé au lycée par **Leul Mulugeta**, **Kidus Beyene** et **Natnael Abebe**.

Cette version est une amélioration de ce projet d'équipe, réalisée par **Leul Mulugeta**, ajoutant la persistance des données avec SQLAlchemy.

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.