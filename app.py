from flask import Flask, render_template, session, redirect, url_for, jsonify, request
from flask_session import Session
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.permanent_session_lifetime = timedelta(minutes=5)

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
        print(users)
        print(user)
        for i in users:
            print(i['username'], user)
            if user == i['username']:
                pw = db.execute("SELECT password, user_id FROM users WHERE username = ?", user)
                print(user)
                if check_password_hash(pw[0]['password'], password):
                    session['user_id'] = pw[0]['user_id']
                    return redirect('/dashboard')
            
                else:
                    alert = "Incorrect username or password."
                    return render_template('login.html', alert = alert) #to add a msg if login credentials are incorrect
        
        alert = "Incorrect username or password"
        return render_template('login.html', alert = alert)

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session["user_id"]
    if request.method == "GET":
        logs = db.execute("SELECT desc, amount FROM log WHERE user_id = ?", user_id)
        bal = db.execute("SELECT balance FROM finance WHERE user_id = ?", user_id)

        return render_template('dashboard.html', logs = logs, bal = bal)
    
    else:
        date = request.form.get("date")
        desc = request.form.get("desc")
        amt = int(request.form.get("amount"))
        type = request.form.get("type")

        if(type == "expense"):
            amt = amt * (-1)

        balance = int(request.form.get("balance"))

        db.execute("INSERT INTO log (user_id, amount, desc, date) VALUES(?, ?, ?, ?)", user_id, amt, desc, date)
        db.execute("UPDATE finance SET balance = ? WHERE user_id = ?", (balance + amt), user_id)


        return redirect('/dashboard')


@app.route('/signup', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = generate_password_hash(request.form.get("password"))

        users = db.execute("SELECT username FROM users")

        for user in users:
            if username in user['username']:
                alert = "Username already exists. Try a different username."
                return render_template('signup.html', alert = alert) #to add a msg if username already exists
            
        db.execute("INSERT INTO users (username, email, password) VALUES(?, ?, ?)", username, email, password)
        id = db.execute("SELECT user_id FROM users WHERE username = ?", username)
        session['user_id'] = id[0]['user_id']
        db.execute("INSERT INTO finance (balance, user_id) VALUES(?, ?)", 0, session["user_id"])
        return redirect('/dashboard')
    
    return render_template("signup.html")

@app.route('/acc')
def account():
    return render_template('account.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

