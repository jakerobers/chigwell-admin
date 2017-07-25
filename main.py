import os
import sqlite3
from flask import Flask, render_template, session, redirect, url_for, escape, request

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'chigwell-admin.db'),
    SECRET_KEY='development key',# TODO: Refactor to another config.
    USERNAME='admin',# TODO: Refactor to another config.
    PASSWORD='default' # TODO: Refactor to another config.
    ))

app.config.from_envvar('ADMIN_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['email'] = request.form['email']
        return redirect(url_for('home'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    # remove the email from the session if it's there
    session.pop('email', None)
    return redirect(url_for('home'))

# set the secret key.  keep this really secret:
app.secret_key = 'werhKABsflwkjqbflkajdsbasjkdfbaslkjdfbaslk'

@app.route('/')
def home():
    if 'email' in session:
        return render_template('home.html')
    else:
        return render_template('login.html')

@app.route('/accounts')
def accounts():
    if 'email' in session:
        return render_template('accounts.html')
    else:
        return render_template('login.html')


@app.route('/expenses')
def expenses():
    if 'email' in session:
        return render_template('expenses.html')
    else:
        return render_template('login.html')


@app.route('/depreciation')
def depreciation():
    if 'email' in session:
        return render_template('depreciation.html')
    else:
        return render_template('login.html')


@app.route('/peeps')
def peeps():
    if 'email' in session:
        return render_template('peeps.html')
    else:
        return render_template('login.html')

@app.route('/settings')
def settings():
    if 'email' in session:
        return render_template('settings.html')
    else:
        return render_template('login.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
