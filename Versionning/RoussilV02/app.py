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
        db.session.commit() # <-- mise à jour de la base de données
        return redirect(url_for('connexion'))
    return render_template('creation.html')


@app.route('/formulaire')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    return render_template('formulaire.html', username=username)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
