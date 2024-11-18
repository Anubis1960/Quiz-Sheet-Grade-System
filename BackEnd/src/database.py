import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firestore Admin
cred = credentials.Certificate('/home/catalin/Downloads/quiz-grader-firebase-adminsdk-jbul6-4bd261f030.json')

app = firebase_admin.initialize_app(cred)

# Firestore client instance
db = firestore.client()
