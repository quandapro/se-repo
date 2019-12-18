from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'thisissecret'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'retinadb'

mysql = MySQL(app)

@app.route("/")
def index():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('home'))

# Login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))

        account = cursor.fetchone()
        print("account")

        if account:
            session['loggedin'] = True
            session['username'] = account['username']

            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'

    return render_template('login.html', msg=msg)

# Logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# Home
@app.route('/home')
def home():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if session['username'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users')
        accounts = cursor.fetchall()
        print(accounts)
    return render_template('home.html', username=session['username'], accounts=accounts, len = len(accounts))

@app.route('/doctor', methods=['POST'])
def doctor():
    msg = ''
    if 'username' not in session or session['username'] != 'admin':
        msg = 'You are not admin!'
        return redirect(url_for('login'))
    else:
        # ADD DOCTOR
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists!'
            else :
                cursor.execute('INSERT INTO users VALUES (%s, %s)', (username, password))
                mysql.connection.commit()
                msg = 'You have successfully registered!'

    print(msg)
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(port= 8080)