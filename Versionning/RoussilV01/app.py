from flask import Flask,render_template

app=Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/connexion')
def connexion():
    return render_template('connexion.html')

@app.route('/creation')
def creation():
    return render_template('creation.html')

if __name__ ==" __main__ ":
    app.run()
