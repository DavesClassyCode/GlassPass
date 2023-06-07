from app import app, db
from flask import Blueprint, render_template, request, redirect, url_for, Flask, make_response, session
from DBUserHandler import DBHandler
from exceptions import *
import sqlite3

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


@app.route("/information")
def information():
    return render_template("information.html")

@app.route("/times")
def times():
    if "username" in session:
        username = session["username"]
    return render_template("times.html")

@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        """
        userCookie = request.form['username']
        resp = make_response("username")
        resp.set_cookie('username', userCookie)
        """
        session["username"] = username    
        try:
            db = DBHandler()
            if db.attemptLogin(password, Username=username):
                print('successful login')
                return render_template('times.html')
            else:
                print('unsuccessful login')
                return render_template('login.html')
        except FileNotFoundError as e:
            print(e)
            return render_template("login.html")
        except UnsanitaryInputException as e:
            print(e)
            return render_template("login.html")
        except BadPasswordException as e:
            print(e)
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/accountCreated", methods=['POST','GET'])
def accountCreated():
    return render_template('accountCreated.html')

@app.route("/createAccount", methods=['POST','GET'])
def createAccount():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        try:
            db = DBHandler()
            if db.insertNewUserData(firstname, lastname, username, email, password):
                return redirect(url_for('accountCreated'))
        except FileNotFoundError as e:
            print(e)
            return render_template("createAccount.html")
        except UnsanitaryInputException as e:
            print(e)
            return render_template("createAccount.html")
        except BadPasswordException as e:
            print(e)
            return render_template("createAccount.html")
        except sqlite3.DataError as e:
            print(e)
            return render_template("createAccount.html")
    else:
        return render_template("createAccount.html")

@app.route('/logout')
def logout():
    session.pop("username", None)
    return render_template("index.html")


