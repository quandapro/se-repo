from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, get_flashed_messages
from flask_mysqldb import MySQL
# from flask_socketio import SocketIO

import MySQLdb.cursors
import re

import os
import cv2

import image_processing.filters as filters
import image_processing.preprocessing as preprocessing
import image_processing.to_domain as to_domain

import time

# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

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
processed_images = {}

@app.route("/index")
@app.route("/")
def index():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if session['username'] == 'admin':
        return redirect(url_for('admin'))
    return redirect(url_for('browser'))

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

        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            if session['username'] == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('browser'))
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
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM users WHERE username = %s', (username,))
        mysql.connection.commit()
    return redirect(url_for('admin'))

@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    if 'username' not in session or session['username'] == 'admin':
        return redirect(url_for('index')) 

    # Submit diagnosis
    if request.method == 'POST' and 'diagnosis' in request.form and 'id' in request.args:
        diagnosis = request.form['diagnosis']
        patientID = request.args['id']
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO patient VALUES (%s, %s, %s)', (patientID, diagnosis, session['username']))
            mysql.connection.commit()
        except:
            flash("Submit error!")
            return redirect(url_for('doctor', id=patientID))
        flash("Submit success!")
        return redirect(url_for('doctor', id=patientID))

    # Load default image if image is not present in args
    image_filename = '0e0003ddd8df.png'
    if 'id' in request.args:
        image_filename = request.args['id'] + '.png'

    patientID = image_filename.split('.')[0]
    
    image_path = url_for('static', filename='images/' + image_filename)
    image = cv2.imread(os.path.join('static/images', image_filename ))
    auto_predict = 0
    if image_filename in predicted:
        auto_predict = predicted[image_filename]
    else:
        auto_predict = predictor.predict(image)[0] * 100
        predicted[image_filename] = auto_predict
    final_prediction = "%.3f %s" % (auto_predict, '%  (Auto diagnosis)')
    return render_template('doctor.html', image=image_path, predict=final_prediction, username=session['username'], patientID=request.args['id'])

@app.route('/image', methods=['POST'])
def image():
    if 'username' not in session or session['username'] == 'admin':
        return jsonify("Permission denied!")
    now = int(round(time.time() * 1000))
    if request.method == "POST":
        original_image = request.form['image']
        image_path = './static/images/' + original_image
        image = cv2.imread(image_path)
        image = preprocessing.optimize_preprocess(image)

        req_str = request.form['data']

        if 'log-trans' in req_str:
            image = to_domain.log_transform(image)
        if 'freg-domain' in req_str:
            image = to_domain.to_frequency_domain(image)
        if 'to-negative' in req_str:
            image = to_domain.to_negative(image)
        if 'high-pass' in req_str:
            image = filters.high_pass_filter(image)
        if 'laplacian' in req_str:
            image = filters.laplace(image)
        if 'kernel-1' in req_str:
            image = filters.sharpening(image, 1)
        if 'kernel-2' in req_str:
            image = filters.sharpening(image, 2)
        if 'kernel-3' in req_str:
            image = filters.sharpening(image, 3)
        
        new_image = "{}_processed.png".format(str(now))
        cv2.imwrite('./static/images/' + new_image, image)

        return jsonify(url_for('static', filename='images/' + new_image))

@app.route('/browser', methods=['GET'])
def browser():
    if 'username' not in session or session['username'] == 'admin':
        return redirect(url_for('index'))
    image_folder = './static/images/'
    client_folder = '/static/images/'
    files = os.listdir(image_folder)
    images = []
    for filename in files:
        # Skip processed images
        if 'processed' not in filename and ('png' in filename or 'jpg' in filename):
            images.append(filename)
    client_images_path = [client_folder + x for x in images]

    patientID = [x.split('.')[0] for x in images]
    return render_template('browser.html', images=images, patientID=patientID, images_path=client_images_path, length=len(images), username=session['username'])


if __name__ == "__main__":
    app.run(port=5000)