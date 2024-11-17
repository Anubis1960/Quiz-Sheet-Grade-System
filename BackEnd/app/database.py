import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firestore Admin
cred = credentials.Certificate('/home/robertilea/work/serviceAccountKey.json')

app = firebase_admin.initialize_app(cred)

# Firestore client instance
db = firestore.client()
