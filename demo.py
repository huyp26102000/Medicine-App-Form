import firebase_admin
from firebase_admin import credentials, firestore, auth
auth = firebase.auth()
email='demo@gmail.com'
password = '123456'
cred = credentials.Certificate("./inspiration/serviceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)
# db = firestore.client()
# user = auth.create_user(email='demo@gmail.com', password = '123456')
# print()
user = auth.sign_in_with_email_and_password(email, password)