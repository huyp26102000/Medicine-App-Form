import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import hashlib

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
# def submidGeneralInfor(ID, fullName, Doctor, date):
#     data = {
#         u'ID': ID,
#         u'fullname': fullName,
#         u'Doctor': Doctor,
#         u'date': date
#         }
#     db.collection(u'GeneralInfor').document().set(data)
# def granting(ID, Password):

# print(encryp('admin'))
