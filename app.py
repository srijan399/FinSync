from flask import Flask, render_template, session, redirect, url_for, jsonify, request
from flask_session import Session
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finsync.db")

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('team.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        user = request.form.get("username")
        password = request.form.get("password")

        users = db.execute("SELECT username FROM users")
        
        for i in users:
            if user == i['username']:
                pw = db.execute("SELECT password, user_id FROM users WHERE username = ?", user)

                if check_password_hash(pw[0]['password'], password):
                    session['user_id'] = pw[0]['user_id']
                    return redirect('/dashboard')
            
                else:
                    alert = "Incorrect username or password"
                    return render_template('login.html', alert = alert) #to add a msg if login credentials are incorrect
           
            else:
                alert = "Incorrect username or password"
                return render_template('login.html', alert = alert)
            

if __name__ == '__main__':
    app.run(debug=True)