
# Importer les modules nécessaires
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

# Instancier l'application Flask
app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Instancier SQLAlchemy pour intégrer la base de données à l'application
db = SQLAlchemy(app)

# Configuration de la clé secrète de l'application
app.secret_key = 'super secret key'

# Modèle de données pour les utilisateurs
class User(db.Model):
    # Définir les colonnes de la table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

# Modèle de données pour les tâches
class Task(db.Model):
    # Définir les colonnes de la table
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Initialiser la base de données
def init_db():
    with app.app_context():
        db.create_all()

# Appeler la fonction pour initialiser la base de données
init_db()

# Définir la route pour la page d'accueil
@app.route('/')
def home():
    return render_template('home.html')

# Définir la route pour la page de connexion
@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    # Si la méthode de requête est POST (formulaire soumis)
    if request.method == 'POST':
        # Récupérer les valeurs des champs du formulaire
        username = request.form['username']
        password = request.form['password']
        # Vérifier si un utilisateur avec ces identifiants existe
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # Si oui, enregistrer le nom d'utilisateur dans la session et rediriger vers la page de profil
            session['username'] = user.username
            return redirect(url_for('profile'))
        else:
            # Sinon, afficher un message d'erreur sur la page de connexion
            return render_template('connexion.html', error='Nom utilisateur ou mot de passe invalide')
    # Si la méthode de requête est GET (accéder à la page de connexion)
    return render_template('connexion.html')


@app.route('/creation', methods=['GET', 'POST'])
def creation():
    # Vérifie si la méthode est POST, ce qui signifie qu'un formulaire a été soumis
    if request.method == 'POST':
        # Récupère les champs username, password et password_confirm du formulaire
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['password_confirm']

        # Vérifie que le mot de passe et la confirmation sont identiques
        if password != confirm_password:
            return render_template('creation.html', error="Les mots de passe ne sont pas identiques")

        # Vérifie si l'utilisateur existe déjà dans la base de données
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('creation.html', error='Nom utilisateur déjà existant')

        # Crée un nouvel utilisateur avec les champs récupérés et ajoute-le à la base de données
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Redirige vers la page de connexion
        return redirect(url_for('connexion'))

    # Si la méthode n'est pas POST, cela signifie qu'on doit afficher le formulaire de création d'utilisateur
    return render_template('creation.html')


@app.route('/create_task', methods=['POST'])
def create_task():
    # Récupère les champs title et description du formulaire
    title = request.form['title']
    description = request.form['description']

    # Récupère l'utilisateur actuellement connecté
    user = User.query.filter_by(username=session['username']).first()

    # Crée une nouvelle tâche avec les champs récupérés et l'ID de l'utilisateur
    new_task = Task(title=title, description=description, user_id=user.id)
    db.session.add(new_task)
    db.session.commit()

    # Si la tâche a été créée avec succès, redirige vers la page de liste des tâches
    if new_task.id:
        return redirect(url_for('tasks'))
    else:
        return render_template('formulaire.html', error='Erreur lors de la création de la tâche')


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    # Vérifie si l'utilisateur est connecté
    if 'username' not in session:
        return redirect(url_for('connexion'))

    # Récupère l'utilisateur actuellement connecté
    user = User.query.filter_by(username=session['username']).first()

    # Si la méthode est GET et que le paramètre query est présent dans les arguments de la requête,
    # effectue une recherche sur les tâches de l'utilisateur en fonction de la chaîne de recherche
    if request.method == 'GET' and 'query' in request.args:
        query = request.args['query']
        tasks = Task.query.filter(Task.user_id == user.id).filter(
            Task.title.contains(query) | Task.description.contains(query)
        ).all()
    else:
        # Sinon, récupère toutes les tâches de l'utilisateur
        tasks = Task.query.filter_by(user_id=user.id).all()

    # Affiche la liste des tâches de l'utilisateur
    return render_template('tasks.html', tasks=tasks)


# Définir la route pour la création de tâches
@app.route('/formulaire')
def formulaire():
    if 'username' not in session:
        return redirect(url_for('connexion'))
    return render_template('formulaire.html', username=session['username'])

# Définir la route pour la suppression de tâches
@app.route('/delete_task/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks'))

# Définir la route pour la modification de tâches
@app.route('/edit_task/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get(id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        db.session.commit()
        return redirect(url_for('tasks'))
    return render_template('edit_task.html', task=task)

# Définir la route pour l'affichage et la création de tâches
@app.route('/formulaire', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('connexion'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_task = Task(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()

    username = session['username']
    tasks = Task.query.all()  # récupérer les tâches depuis la base de données
    return render_template('formulaire.html', username=username, tasks=tasks)

# Lancer l'application Flask
if __name__ == "__main__":
    app.run(debug=True)
