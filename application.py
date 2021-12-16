import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

# Configure sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        id = request.form.get("id")
        job = request.form.get("job")
        name = request.form.get("name").strip().title()
        month = int(request.form.get("month"))
        day = int(request.form.get("day"))

        if not request.form.get("name"):
            flash('Please Enter Valid Data 😒', 'warning')

            # Redirect Error Fix
            request.method = "GET"
            return index()

        if day > 31 or day < 1:
            flash('Please Enter Valid Day 😓', 'error')

            # Redirect Error Fix
            request.method = "GET"
            return index()

        if month > 12 or month < 1:
            flash('Please Enter Valid Month 😔', 'error')

            # Redirect Error Fix
            request.method = "GET"
            return index()

        if not name.isalnum() or not name.isalpha():
            flash('Please Enter Valid Name and Check Enter The First Name Only 😕', 'error')

            # Redirect Error Fix
            request.method = "GET"
            return index()

        if job == "delete":
            flash('You have Deleted successfully 😟', 'info')
            db.execute("DELETE FROM birthdays WHERE id = ?", id)
            session['id'] = None
            session['name'] = None

            # Redirect Error Fix
            request.method = "GET"
            return index()

        if job == "edit":
            flash('You have successfully modified your birthday 😄', 'success')
            db.execute("UPDATE birthdays SET name = ?,day = ?, month = ? WHERE id = ?", name, day, month, id)

            # Redirect Error Fix
            request.method = "GET"
            return index()

        if job == "add":
            flash('Congratulations, you have added successfully 🥳', 'success')
            user_id = db.execute("INSERT INTO birthdays (name,month,day) VALUES(?,?,?)", name, month, day)
            session['id'] = user_id
            session['name'] = name

            # Redirect Error Fix
            request.method = "GET"
            return index()
    else:

        # TODO: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)

