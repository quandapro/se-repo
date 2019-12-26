from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

import os
import cv2
from predict import Prediction

predictor = Prediction("model_weights.h5")

app = Flask(__name__)
app.secret_key = 'thisissecret'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'retinadb'

mysql = MySQL(app)

predicted = {}

@app.route("/index")
@app.route("/")
def index():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if session['username'] == 'admin':
        return redirect(url_for('admin'))
    return redirect(url_for('doctor'))

# Login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if 'loggedin' in session:
        return redirect(url_for('index'))
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
            if session['username'] == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('doctor'))
        else:
            msg = 'Incorrect username/password!'

    return render_template('login.html', msg=msg)

# Logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg = ''
    if 'username' not in session or session['username'] != 'admin':
        msg = 'You are not admin!'
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users')
    accounts = cursor.fetchall()
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
            return redirect(url_for('admin', msg=msg))

    return render_template('admin.html', username=session['username'], accounts=accounts, len = len(accounts), msg=msg)

@app.route('/delete')
def delete():
    if session['username'] != 'admin':
        return redirect(url_for('index'))
    if 'username' in request.args and request.args.get('username') != 'admin':
        username = request.args.get('username')
        print(username)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM users WHERE username = %s', (username,))
        mysql.connection.commit()
    return redirect(url_for('admin'))

@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    image_filename = '0e0003ddd8df.png'
    image_path = url_for('static', filename='images/' + image_filename)
    image = cv2.imread(os.path.join('static/images', '0e0003ddd8df.png' ))
    auto_predict = 0
    if image_filename in predicted:
        auto_predict = predicted[image_filename]
    else:
        auto_predict = predictor.predict(image)[0]
        predicted[image_filename] = auto_predict
    final_prediction = "%.3f" % auto_predict
    return render_template('doctor.html', image=image_path, predict=final_prediction)

if __name__ == "__main__":
    app.run(port=5000)