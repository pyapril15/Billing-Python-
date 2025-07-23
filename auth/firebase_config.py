import os
import json
import requests
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore, auth as admin_auth

from config import service_key_path

# Load environment variables from .env file
load_dotenv()


class FirebaseConfig:
    """
    Singleton class for initializing and providing access to Firebase services,
    using only the official Firebase Admin SDK and REST API.
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
        sets up Firebase Admin SDK for Firestore and custom authentication.
        """
        # Firebase configuration from environment
        self.api_key = os.getenv("FIREBASE_API_KEY", "AIzaSyDRTR9GmuvCi-4UhCyZQIhC4DIEFcpb-3U")
        self.project_id = os.getenv("FIREBASE_PROJECT_ID", "billing-app-b7f0e")

        # Firebase Auth REST API endpoints
        self.auth_base_url = f"https://identitytoolkit.googleapis.com/v1/accounts"
        self.signup_url = f"{self.auth_base_url}:signUp?key={self.api_key}"
        self.signin_url = f"{self.auth_base_url}:signInWithPassword?key={self.api_key}"
        self.refresh_url = f"https://securetoken.googleapis.com/v1/token?key={self.api_key}"
        self.reset_password_url = f"{self.auth_base_url}:sendOobCode?key={self.api_key}"
        self.email_verification_url = f"{self.auth_base_url}:sendOobCode?key={self.api_key}"
        self.user_info_url = f"{self.auth_base_url}:lookup?key={self.api_key}"

        # Initialize Firebase Admin SDK
        if not firebase_admin._apps:
            try:
                # Path to service account key JSON file
                cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH", service_key_path)
                if not os.path.exists(cred_path):
                    raise FileNotFoundError(f"Service account key file not found at: {cred_path}")

                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            except Exception as e:
                raise RuntimeError(f"Failed to initialize Firebase Admin SDK: {e}")

        # Firestore client instance
        try:
            self.db = firestore.client()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Firestore client: {e}")

    def make_request(self, url: str, data: dict) -> dict:
        """
        Make a POST request to Firebase REST API.

        Args:
            url (str): The API endpoint URL
            data (dict): Request payload

        Returns:
            dict: Response data

        Raises:
            Exception: If request fails
        """
        try:
            response = requests.post(url, json=data)
            response_data = response.json()

            if response.status_code != 200:
                error_message = response_data.get('error', {}).get('message', 'Unknown error')
                raise Exception(error_message)

            return response_data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {e}")
        except json.JSONDecodeError:
            raise Exception("Invalid response from Firebase")


class FirebaseAuth:
    """
    Firebase authentication wrapper using REST API.
    """

    def __init__(self):
        """
        Initializes the FirebaseAuth instance.
        """
        self.config = FirebaseConfig()
        self.current_user = None

    def create_user_with_email_and_password(self, email: str, password: str) -> dict:
        """
        Create a new user with email and password.

        Args:
            email (str): User's email address
            password (str): User's password

        Returns:
            dict: User data with tokens

        Raises:
            Exception: If signup fails
        """
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        response = self.config.make_request(self.config.signup_url, data)
        return response

    def sign_in_with_email_and_password(self, email: str, password: str) -> dict:
        """
        Sign in user with email and password.

        Args:
            email (str): User's email address
            password (str): User's password

        Returns:
            dict: User data with tokens

        Raises:
            Exception: If signin fails
        """
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        response = self.config.make_request(self.config.signin_url, data)
        return response

    def send_email_verification(self, id_token: str):
        """
        Send email verification to user.

        Args:
            id_token (str): User's ID token

        Raises:
            Exception: If sending verification email fails
        """
        data = {
            "requestType": "VERIFY_EMAIL",
            "idToken": id_token
        }

        self.config.make_request(self.config.email_verification_url, data)

    def send_password_reset_email(self, email: str):
        """
        Send password reset email.

        Args:
            email (str): User's email address

        Raises:
            Exception: If sending reset email fails
        """
        data = {
            "requestType": "PASSWORD_RESET",
            "email": email
        }

        self.config.make_request(self.config.reset_password_url, data)

    def get_account_info(self, id_token: str) -> dict:
        """
        Get user account information.

        Args:
            id_token (str): User's ID token

        Returns:
            dict: User account information

        Raises:
            Exception: If getting account info fails
        """
        data = {
            "idToken": id_token
        }

        response = self.config.make_request(self.config.user_info_url, data)
        return response