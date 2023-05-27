from flask import Blueprint, render_template, request
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
    print("Login Ran")
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Username: {username}, Password: {password}")
        from DBUserHandler import DBHandler
        db = DBHandler('SkateDB.db')
        if not db.attemptLogin(password, "", username):
            return render_template("login.html")
        else:
            return render_template("times.html")
    else: 
        request.method=='GET'
        print("GET: render login.html")
        return render_template("login.html")

@views.route("/createAccount")
def createAccount():
    return render_template("createAccount.html")



@views.route('/register', methods=['POST'])
def register():  
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']  
    from DBUserHandler import DBHandler
    db = DBHandler('SkateDB.db') 
    db.insertNewUserData(firstname, lastname, username, email, password)
    return home()



"""
TODO Finish -- rough draft of method, just getting an idea of how method may work. need post within login.html form 
@views.route('/login', methods=['POST'])
def login():  
    username = request.form['username']
    password = request.form['password']
    from DBUserHandler import DBHandler
    db = DBHandler('SkateDB.db') 
    db.attemptLogin(password, "", username)
    return home()
"""