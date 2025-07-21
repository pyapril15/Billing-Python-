from typing import Optional

from google.cloud.firestore import Client, DocumentSnapshot

from models.bill_model import Bill


class BillRepository:
    """
    Repository class for managing Bill records in Firestore.
    """

    def __init__(self, db: Client):
        """
        Initialize the repository with a Firestore client.

        Args:
            db (Client): An instance of Firestore client.
        """
        self.db = db
        self.collection = self.db.collection("bills")

    def save(self, bill: Bill) -> str:
        """
        Save or update a bill in Firestore using bill_no as the document ID.

        Args:
            bill (Bill): The bill object to be saved.

        Returns:
            str: The bill number used as the document ID.
        """
        try:
            self.collection.document(bill.bill_no).set(bill.to_dict())
            return bill.bill_no
        except Exception as e:
            raise Exception(f"Failed to save bill: {e}")

    def get_by_id(self, bill_no: str) -> Optional[Bill]:
        """
        Retrieve a bill by its unique bill number.

        Args:
            bill_no (str): The document ID (bill number).

        Returns:
            Optional[Bill]: A Bill object if found, else None.
        """
        try:
            doc = self.collection.document(bill_no).get()
            return Bill.from_dict(self._with_id(doc)) if doc.exists else None
        except Exception as e:
            raise Exception(f"Failed to retrieve bill '{bill_no}': {e}")

    def update(self, bill_no: str, updates: dict) -> bool:
        """
        Update specific fields of a bill document.

        Args:
            bill_no (str): The document ID of the bill.
            updates (dict): Fields and values to update.

        Returns:
            bool: True if update is successful.
        """
        try:
            self.collection.document(bill_no).update(updates)
            return True
        except Exception as e:
            raise Exception(f"Failed to update bill '{bill_no}': {e}")

    def delete(self, bill_no: str) -> bool:
        """
        Delete a bill from Firestore.

        Args:
            bill_no (str): The document ID of the bill to delete.

        Returns:
            bool: True if deletion is successful.
        """
        try:
            self.collection.document(bill_no).delete()
            return True
        except Exception as e:
            raise Exception(f"Failed to delete bill '{bill_no}': {e}")

    @staticmethod
    def _with_id(doc: DocumentSnapshot) -> dict:
        """
        Include the document ID as 'bill_no' in the document data.

        Args:
            doc (DocumentSnapshot): The document snapshot from Firestore.

        Returns:
            dict: Document data with 'bill_no' field added.
        """
        data = doc.to_dict()
        if data:
            data["bill_no"] = doc.id
        return data
