from flask import Flask, render_template, session, redirect, url_for, escape, request
app = Flask(__name__)


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
