import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore
import pyrebase

from config import service_key_path

# Load environment variables from .env file
load_dotenv()


class FirebaseConfig:
    """
    Singleton class for initializing and providing access to Firebase services,
    including Authentication (Pyrebase) and Firestore (Admin SDK).
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseConfig, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Initializes Firebase configuration using environment variables,
        sets up Pyrebase for auth and Firebase Admin SDK for Firestore.
        """
        # Firebase configuration from environment
        self.config = {
            "apiKey": os.getenv("FIREBASE_API_KEY", "AIzaSyDRTR9GmuvCi-4UhCyZQIhC4DIEFcpb-3U"),
            "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", "billing-app-b7f0e.firebaseapp.com"),
            "projectId": os.getenv("FIREBASE_PROJECT_ID", "billing-app-b7f0e"),
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", "billing-app-b7f0e.firebasestorage.app"),
            "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", "105342828265"),
            "appId": os.getenv("FIREBASE_APP_ID", "1:105342828265:web:68b30c0acff68fce0d3a78"),
            "databaseURL": os.getenv("FIREBASE_DATABASE_URL", "https://billing-app-b7f0e.firebaseio.com")
        }

        # Initialize Pyrebase for authentication
        self.firebase = pyrebase.initialize_app(self.config)
        self.auth = self.firebase.auth()

        # Initialize Firestore (Admin SDK)
        if not firebase_admin._apps:
            try:
                # Path to service account key JSON file
                cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH", service_key_path)
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            except Exception as e:
                raise RuntimeError(f"Failed to initialize Firebase Admin SDK: {e}")

        # Firestore client instance
        self.db = firestore.client()
