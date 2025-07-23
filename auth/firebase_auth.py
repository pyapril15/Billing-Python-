from .firebase_config import FirebaseAuth as BaseFirebaseAuth


class FirebaseAuth:
    """
    A wrapper around Firebase authentication functionality,
    including sign-up, login, email verification, and password reset.
    """

    def __init__(self):
        """
        Initializes the FirebaseAuth instance and sets up Firebase authentication.
        """
        self.auth = BaseFirebaseAuth()
        self.current_user = None

    def sign_up(self, email: str, password: str) -> dict:
        """
        Registers a new user with email and password and sends a verification email.

        Args:
            email (str): User's email address.
            password (str): User's password.

        Returns:
            dict: Firebase user object.

        Raises:
            Exception: If sign-up fails or email verification cannot be sent.
        """
        try:
            user = self.auth.create_user_with_email_and_password(email, password)
            self.send_email_verification(user["idToken"])
            return user
        except Exception as e:
            raise Exception(f"Failed to sign up: {e}")

    def send_email_verification(self, id_token: str):
        """
        Sends a verification email to the user.

        Args:
            id_token (str): The ID token of the user.

        Raises:
            Exception: If the verification email cannot be sent.
        """
        try:
            self.auth.send_email_verification(id_token)
        except Exception as e:
            raise Exception(f"Failed to send verification email: {e}")

    def sign_in(self, email: str, password: str) -> dict:
        """
        Logs in a user using email and password, and checks if the email is verified.

        Args:
            email (str): User's email.
            password (str): User's password.

        Returns:
            dict: Firebase user object.

        Raises:
            Exception: If sign-in fails or the email is not verified.
        """
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            id_token = user["idToken"]

            # Verify email is confirmed
            user_info = self.auth.get_account_info(id_token)
            is_verified = user_info["users"][0].get("emailVerified", False)

            if not is_verified:
                raise Exception("Email not verified. Please check your inbox.")

            self.current_user = user
            return user
        except Exception as e:
            raise Exception(f"Sign in failed: {e}")

    def refresh_email_verification_status(self) -> bool:
        """
        Refreshes and checks the current user's email verification status.

        Returns:
            bool: True if email is verified, False otherwise.

        Raises:
            Exception: If refreshing fails or no user is signed in.
        """
        if not self.current_user:
            return False

        try:
            id_token = self.current_user["idToken"]
            user_info = self.auth.get_account_info(id_token)
            return user_info["users"][0].get("emailVerified", False)
        except Exception as e:
            raise Exception(f"Failed to refresh email verification: {e}")

    def reset_password(self, email: str) -> bool:
        """
        Sends a password reset email to the user.

        Args:
            email (str): User's email.

        Returns:
            bool: True if reset email was sent successfully.

        Raises:
            Exception: If the reset process fails.
        """
        try:
            self.auth.send_password_reset_email(email)
            return True
        except Exception as e:
            raise Exception(f"Password reset failed: {e}")

    def sign_out(self):
        """
        Signs out the current user.
        """
        self.current_user = None

    def get_current_user(self) -> dict | None:
        """
        Returns the current logged-in user.

        Returns:
            dict | None: User object or None if not logged in.
        """
        return self.current_user