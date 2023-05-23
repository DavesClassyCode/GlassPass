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