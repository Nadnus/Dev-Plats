from functools import wraps
from flask import Flask, render_template, session, request, redirect, url_for, flash
import os
from threading import Thread
import time
from sqlalchemy import create_engine
from sqlalchemy.dialects import mysql
import hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)


engine = create_engine('mysql+pymysql://localhost')
con = engine.connect()
con.execute("CREATE TABLE IF NOT EXISTS users("+
            "id INTEGER PRIMARY KEY AUTO_INCREMENT,"+
            "username TEXT(50),"+
            "password TEXT(50))")

def user_exists(username):
    result = con.execute("SELECT username FROM users;")
    return username in result

def login_required(f):
    @wraps(f)
    def decor_func(*args, **kwargs):
        if "username" not in session:
            flash("You need to log in!")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decor_func

@app.route("/index")
@login_required
def index():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route("/")
def main():
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("index"))
    if request.method == "POST" and request.form["username"] and request.form["password"]:
        username = request.form["username"]
        password = request.form["password"]
        if(user_exists(username)):
            result = con.execute("SELECT username, password FROM users;")
            m = hashlib.sha256()
            m.update(password)
            passw = m.digest()
            for row in result:
                if username in row and passw in row:
                    session["username"] = username
                    return redirect(url_for("index"))
                else:
                    flash("Incorrect username or password")
                    return render_template("login.html")
        else:
            flash("Incorret username or password")
            return render_template("login.html")
    elif request.method == "POST" and request.form["r_username"] and request.form["r_password"]:
        username = request.form["r_username"]
        password = request.form["r_password"]
        if(user_exists(username)):
            flash("Username already exists")
            return render_template("login.html")
        else:
            m = hashlib.sha256()
            m.update(password)
            passw = m.digest()
            con.execute("INSERT INTO users(username, password) VALUES(" + username + "," + passw + ");")
            flash("Register succesfull")
            return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/users")
def users():
    q = con.execute("SELECT username FROM users;")
    st = ""
    for row in q:
        st += row
        st += ";"
    return st

class Cache():
    def __init__(self, timestamp, time_alive=60*30):
        self.timestamp = timestamp
        self.time_alive = time_alive
        self.data = {}
        self.t = Thread()

    def run(self):
        time.sleep(60*5)
        for key in self.data:
            if self.data[key]["timestamp"] >= time.time()+self.time_alive:
                self.data[key] = None

    def update(self, key, data):
        self.data[key] = data

    def get_users(self, connection):
        result = connection.execute("SELECT username FROM users;")
        self.data["users"] =
    def get_key(self, key, connection):
        if(self.data[key] == None):
            if(key == users):
                self.get_users(connection)
        else:
            return self.data[key]



if __name__ == "__main__":
    app.run()

