import os
import sqlite3
import subprocess
from flask import Flask, render_template, session, redirect, url_for, escape, request, flash

app = Flask(__name__)

# set the secret key.  keep this really secret:
app.secret_key = os.environ["SECRET_KEY"] 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        admin_email = os.environ["ADMIN_EMAIL"]
        admin_password = os.environ["ADMIN_PASSWORD"]
        request_email = ""
        request_password = ""

        if "email" in request.form:
            request_email = request.form["email"]

        if "password" in request.form:
            request_password = request.form["password"]

        if request_email == admin_email and request_password == admin_password:
            session["email"] = request_email
            return redirect(url_for("home"))
        else:
            error = "Incorrect username or password."
            return render_template("login.html", error=error)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    # remove the email from the session if it"s there
    session.pop("email", None)
    return redirect(url_for("home"))


@app.route("/")
def home():
    if "email" in session:
        if "LEDGER_FILE" in os.environ:
            ledger_file = os.environ["LEDGER_FILE"]
            bash_command = "ledger -f " + ledger_file + " balance --no-total"
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            ledger = output.decode(encoding="utf-8", errors="strict")
            ledger = "\n" + ledger

            return render_template("home.html", ledger=ledger)
        else:
            error = "The LEDGER_FILE env variable must be defined."
            return render_template("home.html", error=error)
    else:
        return render_template("login.html")

@app.route("/accounts")
def accounts():
    if "email" in session:
        if "LEDGER_FILE" in os.environ:
            ledger_file = os.environ["LEDGER_FILE"]
            bash_command = "ledger -f " + ledger_file + " accounts"
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            ledger = output.decode(encoding="utf-8", errors="strict")
            ledger = "\n" + ledger

            return render_template("accounts.html", ledger=ledger)
        else:
            error = "The LEDGER_FILE env variable must be defined."
            return render_template("accounts.html", error=error)
    else:
        return render_template("login.html")


@app.route("/expenses")
def expenses():
    if "email" in session:
        if "LEDGER_FILE" in os.environ:
            ledger_file = os.environ["LEDGER_FILE"]
            bash_command = "ledger -fc " + ledger_file + " reg"
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            ledger = output.decode(encoding="utf-8", errors="strict")
            ledger = "\n" + ledger

            return render_template("expenses.html", ledger=ledger)
        else:
            error = "The LEDGER_FILE env variable must be defined."
            return render_template("expenses.html", error=error)
    else:
        return render_template("login.html")


@app.route("/depreciation")
def depreciation():
    if "email" in session:
        return render_template("depreciation.html")
    else:
        return render_template("login.html")


@app.route("/peeps")
def peeps():
    if "email" in session:
        return render_template("peeps.html")
    else:
        return render_template("login.html")

@app.route("/settings")
def settings():
    if "email" in session:
        return render_template("settings.html")
    else:
        return render_template("login.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404
