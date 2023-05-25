from flask import Blueprint, render_template, request

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

@views.route("/login")
def login():
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
    #getting strings from the create account form
    #TODO enter information into the user table within DB