from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'super secret key'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))




def init_db():
    with app.app_context():
        db.create_all()


init_db()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = user.username
            return redirect(url_for('profile'))
        else:
            return render_template('connexion.html', error='Invalid username or password')
    return render_template('connexion.html')


@app.route('/creation', methods=['GET', 'POST'])
def creation():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['password_confirm']
        if password != confirm_password:
            return render_template('creation.html', error="Passwords don't match")
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('creation.html', error='Username already exists')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('connexion'))
    return render_template('creation.html')

@app.route('/create_task', methods=['POST'])
def create_task():
    title = request.form['title']
    description = request.form['description']
    user = User.query.filter_by(username=session['username']).first()
    new_task = Task(title=title, description=description, user_id=user.id)
    db.session.add(new_task)
    db.session.commit()
    if new_task.id:
        return redirect(url_for('tasks'))
    else:
        return render_template('formulaire.html', error='Error creating task')

@app.route('/tasks')
def tasks():
    if 'username' not in session:
        return redirect(url_for('connexion'))
    user = User.query.filter_by(username=session['username']).first()
    tasks = Task.query.filter_by(user_id=user.id).all()
    return render_template('tasks.html', tasks=tasks)


@app.route('/formulaire')
def formulaire():
    if 'username' not in session:
        return redirect(url_for('connexion'))
    return render_template('formulaire.html', username=session['username'])




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


if __name__ == "__main__":
    app.run(debug=True)
