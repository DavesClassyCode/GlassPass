from flask import Blueprint, render_template, request
from DBUserHandler import DBHandler
from exceptions import *
import sqlite3

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/pricing")
def pricing():
    return render_template("pricing.html")


@views.route("/information")
def information():
    return render_template("information.html")

@views.route("/times")
def times():
    return render_template("times.html")

@views.route("/login", methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['userName']
        password = request.form['password']
        try:
            db = DBHandler('SkateDB.db')
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
        # if not db.attemptLogin(password, "", username):
        #     print("Unsuccessful Login attempt")
        #     return render_template("login.html")
        # else:
        #     print("Login Success!")
        #     return render_template("times.html")
    else:
        request.method=='GET'
        # print("GET: render login.html")
        return render_template("login.html")

@views.route("/createAccount", methods=['POST','GET'])
def createAccount():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        try:
            db = DBHandler('SkateDB.db')
            if db.insertNewUserData(firstname, lastname, username, email, password):
                return render_template("times.html")
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

# @views.route('/register', methods=['POST'])
# def register():
#     # firstname = request.form['firstname']
#     # lastname = request.form['lastname']
#     # username = request.form['username']
#     # password = request.form['password']
#     # email = request.form['email']
#     # try:
#     #     db = DBHandler('SkateDB.db')
#     #     if db.insertNewUserData(firstname, lastname, username, email, password):
#     #         return render_template("times.html")
#     # except FileNotFoundError as e:
#     #     print(e)
#     # except UnsanitaryInputException as e:
#     #     print(e)
#     # except BadPasswordException as e:
#     #     print(e)
#     # except sqlite3.DataError as e:
#     #     print(e)
#     # finally:
#     #     del db
#     return render_template("createAccount.html")


