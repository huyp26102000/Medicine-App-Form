import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
from model import *
from datetime import datetime

cred = credentials.Certificate("./inspiration/serviceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

def validLogin(ID, Password):
    docs = db.collection(u'Account').stream()
    for doc in docs:
        if ID == doc.to_dict()['username'] and Password == doc.to_dict()['Password']:
                print("true")
                return True
    return False
def getBox1Infor():
    docs = db.collection(u'GeneralInfor').stream()
    allDoc = list(docs)
    for i in range(0, len(allDoc)):
        allDoc[i] = allDoc[i].to_dict()
        allDoc[i]['date'] = datetime.strptime(allDoc[i]['date'], '%d/%m/%y')
    tmp = allDoc[0]
    for i in range(1, len(allDoc)):
        if(tmp['date'] < allDoc[i]['date']):
            tmp = allDoc[i]
    return tmp

    # print(allDoc)
def encryp(string_to_hash):
    hash_object = hashlib.sha256(str(string_to_hash).encode('utf-8'))
    return hash_object.hexdigest()
def submidGeneralInfor(ID, fullName, Doctor, date):
    data = {
        u'ID': ID,
        u'fullname': fullName,
        u'Doctor': Doctor,
        u'date': date
        }
    db.collection(u'GeneralInfor').document().set(data)
def submidGeneralInfor(ID, fullName, Doctor, date):
    data = {
        u'ID': ID,
        u'fullname': fullName,
        u'Doctor': Doctor,
        u'date': date
        }
    db.collection(u'GeneralInfor').document().set(data)
# def granting(ID, Password):

# submidGeneralInfor('asdasdasdasd', 'demoName', 'demo2', '1-Nov-18')
# getBox1Infor()
