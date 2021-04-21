import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
from model import *
from datetime import datetime
import uuid

cred = credentials.Certificate("./inspiration/serviceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

def getNewID():
    id = uuid.uuid4()
    return str(id)
def getAllPatient():
    docs = db.collection(u'Account').where(u'role', u'==', 1).stream()
    allDoc = list(docs)
    for i in range(0, len(allDoc)):
        allDoc[i] = allDoc[i].to_dict()
        allDoc[i]['role'] = 'Patient'
        if allDoc[i]['status'] == 0:
            allDoc[i]['status'] = 'Active'
    return allDoc
def searchPatient(key):
    docs = db.collection(u'Account').stream()
    allDoc = list(docs)
    found = []
    for i in range(0, len(allDoc)):
        allDoc[i] = allDoc[i].to_dict()
        if ((key in allDoc[i]['phone'])
            or (key in allDoc[i]['email'])
            or (key in allDoc[i]['fullname'])
            or (key in allDoc[i]['username'])):
                found.append(allDoc[i])
    return found)

def validLogin(ID, Password):
    docs = db.collection(u'Account').stream()
    allDoc = list(docs)
    for doc in allDoc:
        # print(doc.to_dict())
        if ID == doc.to_dict()['username'] and Password == doc.to_dict()['Password']:
            return doc.to_dict()
    return None
# validLogin('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918')
def get_Newest_Med_Infor(PatientID):
    docs = db.collection(u'Med_Infor').stream()
    allDoc = list(docs)
    for i in range(0, len(allDoc)):
        allDoc[i] = allDoc[i].to_dict()
        allDoc[i]['date'] = datetime.strptime(allDoc[i]['date'], '%d/%m/%y')
    tmp = allDoc[0]
    for i in range(1, len(allDoc)):
        if(tmp['date'] < allDoc[i]['date'] and tmp['ID']==PatientID):
            tmp = sortPatient[i]
    return tmp
def encryp(string_to_hash):
    hash_object = hashlib.sha256(str(string_to_hash).encode('utf-8'))
    return hash_object.hexdigest()
def submit_NewMed_Infor(ID, fullName, Doctor, date):
    MedID = getNewID()
    data = {
        u'ID': ID,
        u'MedID': MedID,
        u'fullname': fullName,
        u'Doctor': Doctor,
        u'date': date
        }
    db.collection(u'Med_Infor').document().set(data)
    return MedID
def submidWhenGood( MedID,
                    daily_Med_1,
                    daily_Med_Num_1,
                    daily_Med_use_1,
                    daily_Med_2,
                    daily_Med_Num_2,
                    daily_Med_use_2,
                    reliever_Med):
    data = {
        u'MedID': MedID,
        u'daily_Med_1': daily_Med_1,
        u'daily_Med_Num_1': daily_Med_Num_1,
        u'daily_Med_use_1': daily_Med_use_1,
        u'daily_Med_2': daily_Med_2,
        u'daily_Med_Num_2': daily_Med_Num_2,
        u'daily_Med_use_2': daily_Med_use_2,
        u'reliever_Med': reliever_Med
        }
    db.collection(u'Medicine_WhenGood').document().set(data)
def getMed_WhenGood(MedID):
    docs = db.collection(u'Medicine_WhenGood').stream()
    allDoc = list(docs)
    for i in range(0, len(allDoc)):
        allDoc[i] = allDoc[i].to_dict()
    for tmp in allDoc:
        if(tmp['MedID']==MedID): return(tmp)
    return None
def submidWhenNotgood(  MedID,
                        addMed,
                        addMed_Num,
                        addMed_use):
    data = {
        u'MedID': MedID,
        u'addMed': addMed,
        u'addMed_Num': addMed_Num,
        u'addMed_use': addMed_use
        }
    db.collection(u'Medicine_WhenNotGood').document().set(data)
def getMed_WhenNotgood(MedID):
    docs = db.collection(u'Medicine_WhenNotGood').stream()
    allDoc = list(docs)
    for i in range(0, len(allDoc)):
        allDoc[i] = allDoc[i].to_dict()
    for tmp in allDoc:
        if(tmp['MedID']==MedID): return(tmp)
    return None
def submidWhenBad(  MedID,
                    Prednisone_time,
                    Prednisone_num,
                    Prednisone_days,
                    Methylprednisolon_time,
                    Methylprednisolon_num,
                    Methylprednisolon_days,
                    ):
    data = {
        u'MedID': MedID,
        u'Prednisone_time': Prednisone_time,
        u'Prednisone_num': Prednisone_num,
        u'Prednisone_days': Prednisone_days,
        u'Methylprednisolon_time': Methylprednisolon_time,
        u'Methylprednisolon_num': Methylprednisolon_num,
        u'Methylprednisolon_days': Methylprednisolon_days,
        }
    db.collection(u'Medicine_WhenBad').document().set(data)
def getMed_WhenBad(MedID):
    docs = db.collection(u'Medicine_WhenBad').stream()
    allDoc = list(docs)
    for i in range(0, len(allDoc)):
        allDoc[i] = allDoc[i].to_dict()
    for tmp in allDoc:
        if(tmp['MedID']==MedID): return(tmp)
    return None
def register(Password, avatarURL, fullname, role, username):
    ID = getNewID()
    data = {
        u'ID': ID,
        u'username': username,
        u'fullname': fullname,
        u'Password': Password,
        u'avatarURL': avatarURL,
        u'role': role
        }
    db.collection(u'Account').document().set(data)
# register(   '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',
#             'http://194.62.98.23:8000/open/shared/Bcare.Assets/img/unknowUser.jpg',
#             'Guess 2',
#             1,
#             'guess2'
#             )
# print(getMed_WhenGood(get_Newest_Med_Infor('asdasdasdasd')['MedID']))
# submidWhenGood(submit_NewMed_Infor('asdasdasdasd', 'Hoang', 'demo2', '8/9/20'),
#                 '3','5','3','2','2','2','dbcsssdd')
# submidWhenNotgood(submit_NewMed_Infor('8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Hoang', 'demo2', '8/9/20'),
#                 'yyyy','5','3')
# submidWhenNotgood('')
# getMed_WhenGood('abc')
# getMed_WhenNotgood('7f07f700-b40c-420d-b843-87843f3534fe')
# submidWhenBad('7f07f700-b40c-420d-b843-87843f3534fe',
#                 3, 3, 4, 4, 5, 5)
# print(len(getAllPatient()))
# import random
# #Generate 5 random numbers between 10 and 30
# randomlist = random.sample(range(0, 10), 10)
# print(randomlist)