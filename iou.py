import os
from flask import Flask, render_template, json, request, redirect, url_for, session, send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pymysql
import re
from io import BytesIO
from datetime import date, timedelta, datetime

from util.Calendar import Calendar
from util.IO import IO

app = Flask(__name__)

app.secret_key = "get dogged on"
#Change these values to ours
"""
app.config['MySQL_HOST'] = "localhost"
app.config['MySQL_USER'] = "noahf"
app.config['MySQL_PASSWORD'] = "1"
app.config['MySQL_DB'] = "IOU_DB"
"""

print(app)

# mysql = MySQL(app)

mysql = pymysql.connect(database ='IOU_DB',
                        host='localhost',
                        user='noahf',
                        password='1')

class calPage:
    def __init__(self):
        self.firstDay = date.today()

cp = calPage()

@app.route('/', methods=['GET','POST'])
def main():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']


        cursor = mysql.cursor() #mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM USERNAME WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        #Change keys to noahs database
        if account:
            session['LoggedIn'] = True
            # session['id'] = account['id']
            session['username'] = account[0]
            session['firstName'] = account[1]
            session['lastName'] = account[2]
            return redirect(url_for('home'))

        else:
            msg = 'Incorrect username/password'


    return render_template('index.html', msg=msg)


@app.route('/register', methods=['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'lastName' in request.form and 'firstName' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        lastName = request.form['lastName']
        firstName = request.form['firstName']

        # Check if account exists using MySQL
        cursor = mysql.cursor() #mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM USERNAME WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not firstName or not lastName:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO USERNAME VALUES (%s, %s, %s, %s, %s, false)', (username, firstName, lastName, email, password))
            mysql.commit() #.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'PLEASE PLEASE, do the form!!!'

    return render_template('register.html', msg=msg)

@app.route('/home')
def home():
    msg = ""
    if 'LoggedIn' in session:
        user = session['username']
        try:
            io = IO(user)
            io.queryOweTable()
        except ValueError as v:
            msg = v
        return render_template('home.html', username=user, msg=msg, firstName=session['firstName'])
    return redirect(url_for('login'))

@app.route('/table')
def table():
    # converting csv to html
    msg = ""
    user = session['username']
    io = IO(user)
    fig = io.queryOweTable()

    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/tableReq')
def tableReq():
    # converting csv to html
    msg = ""
    user = session['username']
    io = IO(user)
    fig = io.queryRequestTable()

    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


@app.route('/prev')
def prev():
    cp.firstDay = cp.firstDay - timedelta(days=1)
    return redirect(url_for('home'))

@app.route('/next')
def next():
    cp.firstDay = cp.firstDay + timedelta(days=1)
    return redirect(url_for('home'))

@app.route('/prevReq')
def prevReq():
    cp.firstDay = cp.firstDay - timedelta(days=1)
    return redirect(url_for('viewRequests'))

@app.route('/nextReq')
def nextReq():
    cp.firstDay = cp.firstDay + timedelta(days=1)
    return redirect(url_for('viewRequests'))

@app.route('/fig')
def fig():
    user = session['username']
    cal = Calendar(user)

    fig = cal.plotEvents(cp.firstDay)

    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/home/event', methods=['GET','POST'])
def event():
    msg = ""
    if request.method == 'POST' and 'eventName' in request.form and 'startTime' in request.form and 'endTime' in request.form and 'startDate' in request.form:
        eventName = request.form['eventName']
        startTime = request.form['startTime']
        endTime = request.form['endTime']
        startDate = request.form['startDate']
        # Add to SQL db
        try:
            io = IO(session['username'])
            io.writeNewEvent('EVENT_TABLE', eventName, startTime, endTime, startDate)
            msg = 'Event Added'
        except ValueError as v:
            msg = v
    elif request.method == 'POST':
        msg = 'PLEASE PLEASE, do the form!!!'

    return render_template('event.html', msg = msg)

@app.route('/home/eventRemove', methods=['GET', 'POST'])
def eventRemove():
    msg = ""
    if request.method == 'POST' and 'eventName' in request.form and 'startDate' in request.form:
        eventName = request.form['eventName']
        startDate = request.form['startDate']
        # Add to SQL db
        io = IO(session['username'])
        io.removeEvent(eventName, startDate)
        msg = 'Event Removed'
    elif request.method == 'POST':
        msg = 'PLEASE PLEASE, do the form!!!'
    return render_template('eventRemove.html', msg = msg)

@app.route('/home/requestMake', methods=['GET', 'POST'])
def requestMake():
    msg = ""
    if request.method == 'POST' and 'eventName' in request.form and 'startTime' in request.form and 'endTime' in request.form and 'startDate' in request.form:
        eventName = request.form['eventName']
        startTime = request.form['startTime']
        endTime = request.form['endTime']
        startDate = request.form['startDate']
        # Add to SQL db
        io = IO(session['username'])
        io.addRequest(startDate, startTime, endTime, eventName)
        msg = 'Request Made'
    elif request.method == 'POST':
        msg = 'PLEASE PLEASE, do the form!!!'
    return render_template('requestMake.html', msg=msg)

@app.route('/home/viewRequests')
def viewRequests():
    return render_template('viewRequests.html')

@app.route('/home/viewRequests/fulfill', methods=['GET', 'POST'])
def fulfill():
    msg = ''
    if request.method == 'POST' and 'startDate' in request.form and 'eventName' in request.form and 'otherFirstName' in request.form and 'otherLastName' in request.form:
        otherFirst = request.form['otherFirstName']
        otherLast = request.form['otherLastName']
        startDate = request.form['startDate']
        eventName = request.form['eventName']

        io = IO(session['username'])
        io.fulfill(eventName, startDate, otherFirst, otherLast)

        msg = 'Fulfilled Event!'
    elif request.method == 'POST':
        msg = 'PLEASE PLEASE, do the time!!!'
    return render_template('fulfill.html', msg=msg)

@app.route('/logout')
def logout():

    usr = session['username']
    #os.remove(f'images/calendar-{usr}')
    session.pop('LoggedIn', None)
    #session.pop('id', None)
    session.pop('username', None)

    return redirect(url_for('main'))


if __name__ == "__main__":
    app.run()
