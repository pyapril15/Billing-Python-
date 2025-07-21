from typing import Optional, List

from auth.firebase_config import FirebaseConfig
from models.bill_model import Bill
from repositories.bill_repository import BillRepository


class BillService:
    """
    Service layer for managing business logic related to Bill operations.
    """

    def __init__(self):
        """
        Initializes Firestore database and sets up the Bill repository.
        """
        firebase_config = FirebaseConfig()
        self.db = firebase_config.db
        self.repo = BillRepository(self.db)

    def create_bill(self, bill: Bill) -> bool:
        """
        Create and save a new bill.

        Args:
            bill (Bill): Bill object to be saved.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.repo.save(bill)
            return True
        except Exception as e:
            print(f"[create_bill] Error creating bill: {e}")
            return False

    def get_bill(self, bill_no: str) -> Optional[Bill]:
        """
        Retrieve a bill by its bill number.

        Args:
            bill_no (str): Unique bill number.

        Returns:
            Optional[Bill]: Bill object if found, else None.
        """
        try:
            return self.repo.get_by_id(bill_no)
        except Exception as e:
            print(f"[get_bill] Error retrieving bill '{bill_no}': {e}")
            return None

    def update_bill(self, bill_no: str, updates: dict) -> bool:
        """
        Update an existing bill with provided fields.

        Args:
            bill_no (str): Bill number to update.
            updates (dict): Dictionary of fields to be updated.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            return self.repo.update(bill_no, updates)
        except Exception as e:
            print(f"[update_bill] Error updating bill '{bill_no}': {e}")
            return False

    def delete_bill(self, bill_no: str) -> bool:
        """
        Delete a bill from the database.

        Args:
            bill_no (str): Bill number to delete.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            return self.repo.delete(bill_no)
        except Exception as e:
            print(f"[delete_bill] Error deleting bill '{bill_no}': {e}")
            return False

    def search_bills(self, field: str, value: str) -> List[Bill]:
        """
        Search for bills that match a specific field and value.

        Args:
            field (str): Field name to search (e.g., 'customer_name').
            value (str): Value to match.

        Returns:
            List[Bill]: List of matching Bill objects.
        """
        try:
            query = self.repo.collection.where(field, "==", value).stream()
            return [Bill.from_dict(doc.to_dict()) for doc in query]
        except Exception as e:
            print(f"[search_bills] Error searching bills by {field}={value}: {e}")
            return []
