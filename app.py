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