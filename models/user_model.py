from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional


@dataclass
class User:
    """
    Represents an authenticated user in the billing system.

    Attributes:
        uid (str): Unique identifier for the user (typically from Firebase).
        email (str): User's email address.
        name (str): Display name of the user.
        is_email_verified (bool): Whether the user's email is verified.
        created_at (datetime): Account creation timestamp.
        shop_name (str): Name of the user's shop.
        shop_address (str): Address of the user's shop.
    """
    uid: str
    email: str
    name: str
    is_email_verified: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    shop_name: str = ""
    shop_address: str = ""

    @classmethod
    def from_dict(cls, data: Dict) -> Optional['User']:
        """
        Creates a User instance from a dictionary (typically from Firestore).

        Args:
            data (Dict): A dictionary representing the user document.

        Returns:
            Optional[User]: An instance of User if data is valid; otherwise, None.

        Raises:
            ValueError: If required fields are missing or malformed.
        """
        if not data:
            return None

        try:
            return cls(
                uid=data.get('uid', ''),
                email=data.get('email', ''),
                name=data.get('name', ''),
                is_email_verified=data.get('is_email_verified', False),
                created_at=data.get('created_at', datetime.now()),
                shop_name=data.get('shop_name', ''),
                shop_address=data.get('shop_address', '')
            )
        except Exception as e:
            raise ValueError(f"Failed to create User from dict: {e}")

    def to_dict(self) -> Dict:
        """
        Converts the User instance into a dictionary suitable for Firestore storage.

        Returns:
            Dict: A dictionary representation of the User.
        """
        return {
            'uid': self.uid,
            'email': self.email,
            'name': self.name,
            'is_email_verified': self.is_email_verified,
            'created_at': self.created_at,
            'shop_name': self.shop_name,
            'shop_address': self.shop_address
        }
