from auth.firebase_config import FirebaseConfig
from models.user_model import User
from repositories.user_repository import UserRepository


class UserService:
    """
    Service class responsible for managing user-related operations
    such as creation, email verification updates, and user profile updates.
    """

    def __init__(self):
        """
        Initialize the UserService with Firestore DB and UserRepository.
        """
        try:
            firebase_config = FirebaseConfig()
            self.db = firebase_config.db
            self.user_repo = UserRepository(self.db)
        except Exception as e:
            raise Exception(f"Failed to initialize UserService: {e}")

    def create_user(self, user_data: dict, name: str, shop_name: str, shop_address: str):
        """
        Creates a new user entry in Firestore based on the provided authentication data.

        Args:
            user_data (dict): Dictionary containing user authentication data from Firebase.
                              Required keys: 'localId', 'email'.
                              Optional key: 'emailVerified'.
            name (str)
            shop_name (str)
            shop_address (str)

        Raises:
            Exception: If user creation fails.
        """
        try:
            uid = user_data["localId"]
            email = user_data["email"]
            is_verified = user_data.get("emailVerified", False)

            user = User(
                uid=uid,
                email=email,
                name=name,
                is_email_verified=is_verified,
                shop_name=shop_name,
                shop_address=shop_address,
            )

            self.user_repo.save(user)
        except KeyError as ke:
            raise Exception(f"Missing required user data field: {ke}")
        except Exception as e:
            raise Exception(f"Failed to create user in Firestore: {e}")

    def update_email_verification(self, uid: str, is_verified: bool):
        """
        Updates the email verification status of the specified user.

        Args:
            uid (str): User's unique ID.
            is_verified (bool): Email verification status to update.

        Raises:
            Exception: If update operation fails.
        """
        try:
            self.user_repo.update(uid, {"is_email_verified": is_verified})
        except Exception as e:
            raise Exception(f"Failed to update email verification: {e}")

    def update_user_fields(self, uid: str, updates: dict):
        """
        Updates arbitrary fields of a user document.

        Args:
            uid (str): User's unique ID.
            updates (dict): Dictionary of fields to update (e.g., {"name": "Alice"}).

        Raises:
            ValueError: If no updates are provided.
            Exception: If update operation fails.
        """
        try:
            if not updates:
                raise ValueError("No update fields provided.")
            self.user_repo.update(uid, updates)
        except Exception as e:
            raise Exception(f"Failed to update user fields: {e}")

    def get_user_profile(self, uid: str) -> dict:
        """
                Retrieves the user details for a specific user by UID.

                Args:
                    uid (str): The unique identifier of the user.

                Returns:
                    dict:

                Raises:
                    Exception: If retrieval fails or Firestore query encounters an error.
                """
        try:
            user = self.user_repo.get_by_id(uid)
            if not user:
                return {}

            return user.to_dict()
        except Exception as e:
            raise Exception(f"Failed to retrieve user details for UID '{uid}': {e}")

    def get_shop_details(self, uid: str) -> dict:
        """
        Retrieves the shop details for a specific user by UID.

        Args:
            uid (str): The unique identifier of the user.

        Returns:
            dict: A dictionary with 'shop_name' and 'shop_address' if found,
                  or an empty dictionary if user not found or fields are missing.

        Raises:
            Exception: If retrieval fails or Firestore query encounters an error.
        """
        try:
            user = self.user_repo.get_by_id(uid)
            if not user:
                return {}

            return {
                "shop_name": user.shop_name or "",
                "shop_address": user.shop_address or ""
            }
        except Exception as e:
            raise Exception(f"Failed to retrieve shop details for UID '{uid}': {e}")
