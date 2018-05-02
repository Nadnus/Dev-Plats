from functools import wraps
from .User import User
from flask import Flask, render_template, session, request, redirect, url_for, flash
import os
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = os.urandom(24)
Base = declarative_base()
engine = create_engine("sqlite:///:memory", echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if(username == "admin" and password == "qwerty"):
            session["username"] = username
            return redirect(url_for("index"))
        else:
            flash("Incorret username or password")
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))
@app.route("/register")
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.password["password"]
        #Validar que no se ha registrado
        registered = False
        if(registered):
            return
    else:
        b=2


if __name__ == "__main__":
    app.run()
