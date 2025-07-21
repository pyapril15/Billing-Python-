from typing import Optional

from google.cloud.firestore import Client, DocumentSnapshot

from models.user_model import User


class UserRepository:
    """
    Repository class to manage User records in Firestore.
    """

    def __init__(self, db: Client):
        """
        Initialize the repository with a Firestore client.

        Args:
            db (Client): Firestore database client.
        """
        self.db = db
        self.collection = self.db.collection("users")

    def save(self, user: User) -> str:
        """
        Save or update a user document using UID as the document ID.

        Args:
            user (User): User object to be saved.

        Returns:
            str: The UID used as document ID.
        """
        try:
            self.collection.document(user.uid).set(user.to_dict())
            return user.uid
        except Exception as e:
            raise Exception(f"Failed to save user '{user.uid}': {e}")

    def get_by_id(self, uid: str) -> Optional[User]:
        """
        Retrieve a user document by UID.

        Args:
            uid (str): Unique user ID (used as document ID).

        Returns:
            Optional[User]: User object if found, else None.
        """
        try:
            doc = self.collection.document(uid).get()
            return User.from_dict(self._with_id(doc)) if doc.exists else None
        except Exception as e:
            raise Exception(f"Failed to retrieve user '{uid}': {e}")

    def update(self, uid: str, updates: dict) -> bool:
        """
        Update fields in a user document.

        Args:
            uid (str): Document ID of the user.
            updates (dict): Dictionary of fields to update.

        Returns:
            bool: True if update is successful.
        """
        try:
            self.collection.document(uid).update(updates)
            return True
        except Exception as e:
            raise Exception(f"Failed to update user '{uid}': {e}")

    def delete(self, uid: str) -> bool:
        """
        Delete a user document by UID.

        Args:
            uid (str): Document ID of the user.

        Returns:
            bool: True if deletion is successful.
        """
        try:
            self.collection.document(uid).delete()
            return True
        except Exception as e:
            raise Exception(f"Failed to delete user '{uid}': {e}")

    @staticmethod
    def _with_id(doc: DocumentSnapshot) -> dict:
        """
        Attach document ID (UID) to Firestore data.

        Args:
            doc (DocumentSnapshot): Firestore document snapshot.

        Returns:
            dict: Document data with UID added.
        """
        data = doc.to_dict()
        if data is not None:
            data['uid'] = doc.id
        return data
