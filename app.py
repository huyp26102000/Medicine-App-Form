from flask import Flask, render_template, redirect, url_for, request
from account import Account
from function import *
import socket


app = Flask(__name__)
auth = False

@app.route('/')
def welcome():
    return redirect('/login')
 
 
@app.route('/home', methods=['GET', 'POST'])
def home():
    global auth
    if request.method == 'POST':
        auth = False
    if auth==False:
        return redirect(url_for('login'))
    else:
        return render_template('MainForm.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    global auth
    acc = Account(None, None, None)
    if request.method == 'POST':

        return redirect(url_for('login'))
 
# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    ## getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()
    ## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    error = None
    global auth
    if request.method == 'POST':
        if validLogin(request.form['username'], encryp(request.form['password'])) == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            auth = True
        # print(ip_address)
    if auth==False:
        return render_template('loginV2.html', error=error)
    else:
        return redirect(url_for('home'))
    
 
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)