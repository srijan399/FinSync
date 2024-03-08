from flask import Flask, render_template, session, redirect, jsonify, request
from flask_session import Session
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from functools import wraps

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.permanent_session_lifetime = timedelta(days=5)

db = SQL("sqlite:///finsync.db")

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('team.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        if session.permanent:
            return redirect('/dashboard')
        
        else:
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
                    session.permanent = True
                    return redirect('/dashboard')
            
                else:
                    alert = "Incorrect username or password."
                    return render_template('login.html', alert = alert) #to add a msg if login credentials are incorrect
        
        alert = "Incorrect username or password"
        return render_template('login.html', alert = alert)

@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    user_id = session["user_id"]
    if request.method == "GET":
        bal = db.execute("SELECT balance FROM finance WHERE user_id = ?", user_id)

        return render_template('dashboard.html', bal = bal)
    
    else:
        desc = request.form.get("desc")
        amt = int(request.form.get("amount"))
        type = request.form.get("type")
        date = request.form.get("date")

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

        users = db.execute("SELECT username, email FROM users")

        for user in users:
            if username in user['username']:
                return render_template('signup.html', alert = "Username already exists. Try a different username.") #to add a msg if username already exists
            
            elif email in user['email']:
                return render_template('signup.html', alert = "The account already exists with this email.") #to add a msg if email already exists
            
        db.execute("INSERT INTO users (username, email, password) VALUES(?, ?, ?)", username, email, password)
        id = db.execute("SELECT user_id FROM users WHERE username = ?", username)
        session['user_id'] = id[0]['user_id']
        db.execute("INSERT INTO finance (balance, user_id) VALUES(?, ?)", 0, session["user_id"])
        session.permanent = True
        return redirect('/dashboard')
    
    return render_template("signup.html")

@app.route('/acc')
@login_required
def account():
    user_id = session["user_id"]
    detail = db.execute("SELECT username, email FROM users WHERE user_id = ?", user_id)
    return render_template('account.html', detail=detail)

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect('/')

@app.route('/help')
def help():
    return render_template("financial.html")

@app.route('/get_logs', methods=["POST"])
@login_required
def get_log():
    user_id = session["user_id"]
    date = request.form.get("date")

    data = db.execute("SELECT * FROM log WHERE user_id = ? AND date = ?", user_id, date)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)

