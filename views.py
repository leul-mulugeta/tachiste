from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash


# --- Configuration de l'application Flask ---

app = Flask(__name__)
# Clé secrète pour sécuriser les sessions et les cookies
app.config["SECRET_KEY"] = "QWERTY"
# Chemin vers le fichier de base de données SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# Désactive le suivi des modifications de SQLAlchemy (pour de meilleures performances)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialise l'extension SQLAlchemy avec l'application Flask
db = SQLAlchemy(app)


# --- Définition des modèles de base de données ---

class Users(db.Model, UserMixin):
    """
    Modèle pour la table des utilisateurs.
    Hérite de UserMixin pour l'intégration avec Flask-Login.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Définit la relation "un-à-plusieurs" : un utilisateur peut avoir plusieurs tâches
    tasks = db.relationship("Task", backref="user", lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Task(db.Model):
    """
    Modèle pour la table des tâches.
    """

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(300), nullable=False)
    task_datetime = db.Column(db.DateTime, nullable=True)
    favorite = db.Column(db.Boolean, default=False, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    # Clé étrangère qui lie cette tâche à un utilisateur (via l'ID de l'utilisateur)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, task_name, task_datetime, user_id):
        self.task_name = task_name
        self.task_datetime = task_datetime
        self.user_id = user_id
        self.favorite = False
        self.completed = False

# Crée toutes les tables définies dans les modèles (si elles n'existent pas déjà)
with app.app_context():
    db.create_all()


# --- Configuration de Flask-Login ---

login_manager = LoginManager(app)
# Définit la route vers laquelle l'utilisateur est redirigé s'il essaie d'accéder
# à une page protégée sans être connecté.
login_manager.login_view = "login"
# Message flash affiché à l'utilisateur.
login_manager.login_message = "Connectez-vous pour accéder à cette page."
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    """
    Fonction utilisée par Flask-Login pour recharger l'objet utilisateur
    depuis la session, en utilisant l'ID stocké.
    """
    return db.session.get(Users, int(user_id))


# --- Routes principales (Authentification et Pages) ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Gère la connexion de l'utilisateur."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 1. Trouve l'utilisateur par son nom d'utilisateur
        found_user = Users.query.filter_by(username=username).first()

        # 2. Vérifie si l'utilisateur existe ET si le mot de passe fourni
        #    correspond au mot de passe haché dans la base de données.
        if found_user and check_password_hash(found_user.password, password):
            # Enregistre l'utilisateur comme étant connecté
            login_user(found_user)
            # Redirige vers le tableau de bord
            return redirect(url_for("dashboard"))
        flash(
            "Le nom d'utilisateur ou le mot de passe n'est pas correct!",
            category="error",
        )
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Gère l'inscription d'un nouvel utilisateur."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Vérifie si le nom d'utilisateur est déjà pris
        found_user = Users.query.filter_by(username=username).first()

        if found_user:
            flash(
                "Le nom d'utilisateur existe déjà. Veuillez en utiliser un autre.",
                category="error",
            )
        elif len(username) < 2:
            flash(
                "Votre nom d'utilisateur doit être composé d'au moins 2 caractères.",
                category="error",
            )
        else:
            # Sécurité : Hache le mot de passe avant de le stocker
            hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
            user = Users(username, hashed_password)
            # Ajoute le nouvel utilisateur à la session de la base de données
            db.session.add(user)
            # Valide la transaction
            db.session.commit()

            flash("Votre compte a été créé avec succès.", category="success")
            return redirect("login")
    return render_template("register.html")

@app.route("/logout")
@login_required  # L'utilisateur doit être connecté pour se déconnecter
def logout():
    """Déconnecte l'utilisateur."""
    logout_user()
    flash("Vous avez été déconnecté avec succès.", category="success")
    return redirect("login")

@app.route("/dashboard")
@login_required
def dashboard():
    """Tableau de bord principal (page d'accueil après connexion)."""
    return render_template("dashboard.html")


# --- Routes pour la gestion des tâches (CRUD) ---

@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    """
    Affiche toutes les tâches non terminées (GET)
    et gère la création d'une nouvelle tâche (POST).
    """
    if request.method == "POST":
        task_name = request.form.get("task")
        task_datetime_str = request.form.get("schedule")

        task_datetime = None
        if task_datetime_str:
            # Gère les erreurs si le format de la date est invalide
            try:
                task_datetime = datetime.strptime(task_datetime_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                flash("Date ou heure fournie invalide.", "error")
                return redirect(url_for("tasks"))

        # Crée une nouvelle tâche en l'associant à l'utilisateur actuel
        new_task = Task(
            task_name=task_name, task_datetime=task_datetime, user_id=current_user.id
        )

        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for("tasks"))

    # (Méthode GET) Récupère toutes les tâches non terminées de l'utilisateur connecté
    not_completed_tasks = Task.query.filter_by(
        user_id=current_user.id, completed=False
    ).all()

    return render_template("all_tasks.html", task=not_completed_tasks, active="tasks")

@app.route("/tasks/today")
@login_required
def today_tasks():
    """Affiche les tâches prévues pour aujourd'hui."""
    today = datetime.now()
    today_date = today.date()
    
    formatted_date = today.strftime('%A %d %B').title()

    # Récupère les tâches de l'utilisateur...
    today_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        func.date(Task.task_datetime) == today_date,
        Task.completed == False,
    ).all()

    return render_template("today.html", today_tasks=today_tasks, formatted_date=formatted_date, active="today")

@app.route("/tasks/important")
@login_required
def important_tasks():
    """Affiche les tâches marquées comme importantes."""
    important_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        Task.favorite == True,
        Task.completed == False,
    ).all()

    return render_template(
        "important.html", important_tasks=important_tasks, active="important"
    )

@app.route("/tasks/completed")
@login_required
def completed_tasks():
    """Affiche toutes les tâches terminées."""
    completed_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        Task.completed == True,
    ).all()

    return render_template(
        "completed.html", completed_tasks=completed_tasks, active="completed"
    )

@app.route("/delete_task", methods=["POST"])
@login_required
def delete_task():
    """Supprime une tâche."""
    task_id = int(request.form.get("task_id"))
    task = db.session.get(Task, task_id)

    # Vérification de sécurité : la tâche existe ET appartient à l'utilisateur connecté
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()

    # Redirige l'utilisateur vers la page d'où il vient (ex: /tasks ou /tasks/today)
    return redirect(request.referrer or url_for("tasks"))

@app.route("/toggle_important_task", methods=["POST"])
@login_required
def toggle_important_task():
    task_id = int(request.form.get("task_id"))
    task = db.session.get(Task, task_id)

    # Vérification de sécurité
    if task and task.user_id == current_user.id:
        # Inverse la valeur booléenne (True -> False, False -> True)
        task.favorite = not task.favorite
        db.session.commit()

    return redirect(request.referrer or url_for("tasks"))

@app.route("/toggle_task_completed", methods=["POST"])
@login_required
def toggle_task_completed():
    task_id = int(request.form.get("task_id"))
    task = db.session.get(Task, task_id)

    # Vérification de sécurité
    if task and task.user_id == current_user.id:
        task.completed = not task.completed
        db.session.commit()

    return redirect(request.referrer or url_for("tasks"))


if __name__ == "__main__":
    # Lance le serveur de développement Flask
    app.run(debug=True)
