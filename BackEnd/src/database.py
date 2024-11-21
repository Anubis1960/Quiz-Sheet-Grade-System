import firebase_admin
from firebase_admin import credentials, firestore
import os


# Initialize Firestore Admin
key = os.getenv('FIREBASE')
cred = credentials.Certificate(key)

app = firebase_admin.initialize_app(cred)

# Firestore client instance
db = firestore.client()
