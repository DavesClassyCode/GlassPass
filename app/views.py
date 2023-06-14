from app import app
from datetime import timedelta
from flask import render_template, request, redirect, url_for, make_response, session, jsonify, flash
from app.models import Users
from DBUserHandler import DBHandler
from exceptions import *
import sqlite3
import sys
from app import S2_lib as evt


#Render template for times if userID is in session, otherwise render login since user is not logged in
@app.route("/")
def index():
    if "userID" in session.keys():
        userID = session["userID"]
        user = Users.query.filter_by(UID=userID).first()
        message = f'Welcome, { user.FirstName }!'
        return render_template('times.html', message=message, user=user)
    return render_template("login.html")

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


@app.route("/information")
def information():
    return render_template("information.html")


# When routed to times check for userID in session, if found:
# Line 37: Get userID from session
# Line 38: Instantiate user object by querying database for user properties using Users model
# Line 40: Pass user object to render_template for use in times.html
@app.route("/times")
def times():
    userID = None
    if "userID" in session.keys():
        userID = session["userID"]
        user = Users.query.filter_by(UID=userID).first()
        message = f'Welcome, { user.FirstName }!'
        return render_template('times.html', message=message, user=user)
    return render_template("times.html")
# Example for Anderson from David:
# Line 48: User object instantiated with properties from database based on username
# Line 59: 'user=user' user object is passed to render_template for use in times.html
@app.route("/login", methods=['POST'])
def login():
    form = request.form
    user = Users.query.filter_by(Username=form['username']).first()
    message = None
    try:
        if not user:
            message = 'Username not found.'
            return render_template('login.html', message=message)
        if user.check_password(form['password'], form['username']):
            # Here I decided not to put the full user object in the session as it would also contain
            # the hash of the users password. (user.Password = encrypted password)
            session['userID'] = user.UID
            message = f'Welcome, { user.FirstName }!'
            return render_template('times.html', message=message, user=user)
        else:
            message = 'Password was incorrect.'
            return render_template('login.html', message=message)
    except FileNotFoundError as e:
        print(e)
        message = 'File Not Found Error.'
        return render_template('login.html', message=message)
    except UnsanitaryInputException as e:
        print(e)
        message = 'Input contains illegal characters.'
        return render_template('login.html', message=message)
    except BadPasswordException as e:
        print(e)
        message = 'Password must be between 6 and 20 characters and contain at least 1 uppercase letter, 1 lowercase letter, 1 number and 1 special character.'
        return render_template('login.html', message=message)

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
    session.pop("userID", None)
    message = 'Logout Successful'
    return render_template("login.html", message=message)

# (B2) ENDPOINT - GET EVENTS
@app.route("/get/", methods=["POST"])
def get():
  data = dict(request.form)
  events = evt.get(int(data["month"]), int(data["year"]))
  return "{}" if events is None else events

# (B3) ENDPOINT - SAVE EVENT
@app.route("/save/", methods=["POST"])
def save():
  data = dict(request.form)
  print(data)
  ok = evt.save(data["s"], data["e"], data["t"], data["c"], data["b"], data["uid"], data["id"] if "id" in data else None)
  msg = "OK" if ok else sys.last_value
  return make_response(msg, 200)

# (B4) ENDPOINT - DELETE EVENT
@app.route("/delete/", methods=["POST"])
def delete():
  data = dict(request.form)
  ok = evt.delete(data["id"])
  msg = "OK" if ok else sys.last_value
  return make_response(msg, 200)


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)



@app.route("/booking")
def booking():
    if "userID" in session.keys():
        user = session["userID"]
    return render_template("booking.html")


