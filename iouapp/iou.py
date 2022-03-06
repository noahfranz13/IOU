from flask import Flask, render_template, json, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pymysql
import re

app = Flask(__name__)

# app.secret_key = "get dogged on"
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


@app.route('/', methods=['GET','POST'])
def main():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']


        cursor = mysql.cursor() #mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM USERNAME WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return 'Logged in successfully'
        else:
            msg = 'Incorrect username/password'


    return render_template('index.html', msg=msg)


@app.route('/register', methods=['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

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
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO USERNAME VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.commit() #.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'PLEASE PLEASE, do the form!!!'

    return render_template('register.html', msg=msg)

@app.route('/logout')
def logout():

    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    return redirect(url_for('main'))


if __name__ == "__main__":
    app.run()
