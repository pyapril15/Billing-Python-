from typing import Optional

from google.cloud.firestore import Client, DocumentSnapshot

from models.product_model import Product


class ProductRepository:
    """
    Repository class for managing Product records in Firestore.
    """

    def __init__(self, db: Client):
        """
        Initialize the repository with a Firestore client.

        Args:
            db (Client): Firestore database client.
        """
        self.db = db
        self.collection = self.db.collection("products")

    def save(self, product: Product) -> str:
        """
        Save or update a product in Firestore using product_id as document ID.

        Args:
            product (Product): The product object to be saved.

        Returns:
            str: The product_id used as the document ID.
        """
        try:
            self.collection.document(product.product_id).set(product.to_dict())
            return product.product_id
        except Exception as e:
            raise Exception(f"Failed to save product '{product.product_id}': {e}")

    def get_by_id(self, product_id: str) -> Optional[Product]:
        """
        Retrieve a product by its unique product ID.

        Args:
            product_id (str): The document ID (product ID).

        Returns:
            Optional[Product]: A Product object if found, else None.
        """
        try:
            doc = self.collection.document(product_id).get()
            return Product.from_dict(self._with_id(doc)) if doc.exists else None
        except Exception as e:
            raise Exception(f"Failed to retrieve product '{product_id}': {e}")

    def update(self, product_id: str, updates: dict) -> bool:
        """
        Update specific fields of a product document.

        Args:
            product_id (str): The document ID of the product.
            updates (dict): Fields and values to update.

        Returns:
            bool: True if update is successful.
        """
        try:
            self.collection.document(product_id).update(updates)
            return True
        except Exception as e:
            raise Exception(f"Failed to update product '{product_id}': {e}")

    def delete(self, product_id: str) -> bool:
        """
        Delete a product from Firestore.

        Args:
            product_id (str): The document ID of the product to delete.

        Returns:
            bool: True if deletion is successful.
        """
        try:
            self.collection.document(product_id).delete()
            return True
        except Exception as e:
            raise Exception(f"Failed to delete product '{product_id}': {e}")

    @staticmethod
    def _with_id(doc: DocumentSnapshot) -> dict:
        """
        Add the Firestore document ID to the document data.

        Args:
            doc (DocumentSnapshot): The Firestore document snapshot.

        Returns:
            dict: Document data with 'product_id' field added.
        """
        data = doc.to_dict()
        if data:
            data['product_id'] = doc.id
        return data
