from flask import Flask, render_template, redirect, url_for, request,session
from model import *
from function import *
import socket
SESSION_TYPE = 'memcache'

app = Flask(__name__)

@app.route('/')

def welcome():
    return redirect('/showForm')
@app.route('/showForm', methods=['GET', 'POST'])
def showForm():
    tmp = getBox1Infor()
    tmpdate = 'Ngày ' + tmp['date'].strftime("%d") + ' Tháng ' + tmp['date'].strftime("%m") + ' Năm 20' + tmp['date'].strftime("%y")
    if request.method == 'POST':
        return redirect(url_for('login')) 
    else:
        return render_template( 'ShowForm.html',
                                    fullname = tmp['fullname'],
                                    Doctor = tmp['Doctor'],
                                    Date = tmpdate)
 
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['logged_in'] = False
    if not session.get('logged_in'):
        return redirect(url_for('showForm'))
    else:
        return render_template('inputForm.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    acc = Account(None, None, None)
    if request.method == 'POST':
        return redirect(url_for('login'))
 
# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if validLogin(request.form['username'], encryp(request.form['password'])) == False:
            error = 'Invalid Credentials. Please try again.'
            session['logged_in'] = False

        else:
            session['logged_in'] = True
        # print(ip_address)
    if not session.get('logged_in'):
        return render_template('loginV2.html', error=error)
    else:
        return redirect(url_for('home'))
    
 
 
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host='localhost', port=5000, debug=True)