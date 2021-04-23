from flask import Flask, render_template, redirect, url_for, request,session
from model import *
from function import *
import socket
SESSION_TYPE = 'memcache'

app = Flask(__name__)

@app.route('/')

def welcome():
    return redirect('/login')
@app.route('/showForm', methods=['GET', 'POST'])
def showForm():
    session['NewestMed'] = get_Newest_Med_Infor(session.get('identity')['ID'])
    session['tmpDate'] = 'Ngày ' + session.get('NewestMed')['date'].strftime("%d") + ' Tháng ' + session.get('NewestMed')['date'].strftime("%m") + ' Năm 20' + session.get('NewestMed')['date'].strftime("%y")
    session['MedWhenGood'] = getMed_WhenGood(session.get('NewestMed')['MedID'])
    session['MedWhenNotGood'] = getMed_WhenNotgood(session.get('NewestMed')['MedID'])
    session['MedWhenBad'] = getMed_WhenBad(session.get('NewestMed')['MedID'])
    if request.method == 'POST':
        return redirect(url_for('login')) 
    else:
        return render_template('ShowForm.html',
                                fullname = session.get('NewestMed')['fullname'],
                                Doctor = session.get('NewestMed')['Doctor'],
                                Date = session.get('tmpDate'),
                                daily_Med_1 = session.get('MedWhenGood')['daily_Med_1'],
                                daily_Med_Num_1 = session.get('MedWhenGood')['daily_Med_Num_1'],
                                daily_Med_use_1 = session.get('MedWhenGood')['daily_Med_use_1'],
                                daily_Med_2 = session.get('MedWhenGood')['daily_Med_2'],
                                daily_Med_Num_2 = session.get('MedWhenGood')['daily_Med_Num_2'],
                                daily_Med_use_2 = session.get('MedWhenGood')['daily_Med_use_2'],
                                reliever_Med = session.get('MedWhenGood')['reliever_Med'],
                                addMed = session.get('MedWhenNotGood')['addMed'],
                                addMed_Num = session.get('MedWhenNotGood')['addMed_Num'],
                                addMed_use = session.get('MedWhenNotGood')['addMed_use'],
                                Prednisone_time = session.get('MedWhenBad')['Prednisone_time'],
                                Prednisone_num = session.get('MedWhenBad')['Prednisone_num'],
                                Prednisone_days = session.get('MedWhenBad')['Prednisone_days'],
                                Methylprednisolon_time = session.get('MedWhenBad')['Methylprednisolon_time'],
                                Methylprednisolon_num = session.get('MedWhenBad')['Methylprednisolon_num'],
                                Methylprednisolon_days = session.get('MedWhenBad')['Methylprednisolon_days'])

 
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'logout' in request.form:
            session['logged_in'] = False
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('home.html',
                                fullname = session.get('identity')['fullname'],
                                avatarURL = session.get('identity')['avatarURL'])
@app.route('/manager', methods=['GET', 'POST'])
def manager():
    session['patientList'] = []
    if session.get('logged_in'):
        session['patientList'] = getAllPatient()
    if request.method == 'POST':
        if 'logout' in request.form:
            session['logged_in'] = False
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('manager.html',
                                fullname = session.get('identity')['fullname'],
                                avatarURL = session.get('identity')['avatarURL'],
                                listAccount=session.get('patientList')
                                )
@app.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        if 'logout' in request.form:
            session['logged_in'] = False
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('history.html',
                                fullname = session.get('identity')['fullname'],
                                avatarURL = session.get('identity')['avatarURL'])
@app.route('/upplan', methods=['GET', 'POST'])
def upplan():
    if request.method == 'POST':
        if 'logout' in request.form:
            session['logged_in'] = False
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('upplan.html',
                                fullname = session.get('identity')['fullname'],
                                avatarURL = session.get('identity')['avatarURL'])                                

@app.route('/register', methods=['GET', 'POST'])
def register():
    acc = Account(None, None, None)
    if request.method == 'POST':
        return redirect(url_for('login'))
 
# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    session['logged_in'] = False
    if request.method == 'POST':
        session['identity'] = validLogin(request.form['username'], encryp(request.form['password']))
        if  session.get('identity') == None:
            error = 'Invalid Credentials. Please try again.'
            session['logged_in'] = False
        else:
            session['logged_in'] = True
        # print(ip_address)
    if not session.get('logged_in'):
        return render_template('loginV2.html', error=error)
    else:
        if session.get('identity')['role'] == 0:
            return redirect(url_for('home'))
        if session.get('identity')['role'] == 1:
            return redirect(url_for('showForm'))
    
 
 
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host='localhost', port=5000, debug=True)