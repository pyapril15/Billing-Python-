from typing import List, Optional

from auth.firebase_config import FirebaseConfig
from models.product_model import Product
from repositories.product_repository import ProductRepository


class ProductService:
    """
    Service layer for handling product-related business logic.
    """

    def __init__(self):
        """
        Initializes Firestore database and sets up the Product repository.
        """
        firebase_config = FirebaseConfig()
        self.db = firebase_config.db
        self.repo = ProductRepository(self.db)

    def get_all_products(self) -> List[Product]:
        """
        Retrieve all products from the database.

        Returns:
            List[Product]: List of all Product objects.
        """
        try:
            return [self.repo.get_by_id(doc.id) for doc in self.repo.collection.stream()]
        except Exception as e:
            print(f"[get_all_products] Error retrieving products: {e}")
            return []

    def get_products_by_category(self, category: str) -> List[Product]:
        """
        Retrieve products by category.

        Args:
            category (str): Category name to filter products.

        Returns:
            List[Product]: List of Product objects in the given category.
        """
        try:
            query = self.repo.collection.where("category", "==", category).stream()
            return [Product.from_dict(doc.to_dict()) for doc in query]
        except Exception as e:
            print(f"[get_products_by_category] Error fetching products in category '{category}': {e}")
            return []

    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """
        Retrieve a product by its ID.

        Args:
            product_id (str): Unique product ID.

        Returns:
            Optional[Product]: Product object if found, else None.
        """
        try:
            return self.repo.get_by_id(product_id)
        except Exception as e:
            print(f"[get_product_by_id] Error retrieving product '{product_id}': {e}")
            return None

    # Optional: Add this method back if you'd like to preload some default data.
    # def initialize_default_products(self) -> None:
    #     """
    #     Initialize the database with a default set of products if empty.
    #     """
    #     try:
    #         if not list(self.repo.collection.limit(1).stream()):
    #             default_products = [
    #                 Product("med_1", "Sanitizer", 20, "medical"),
    #                 Product("med_2", "Mask", 10, "medical"),
    #                 Product("med_3", "Hand Gloves", 70, "medical"),
    #                 Product("med_4", "Syrup", 30, "medical"),
    #                 Product("med_5", "Cream", 20, "medical"),
    #                 Product("med_6", "Thermal Gun", 20, "medical"),
    #                 Product("gro_1", "Rice", 35, "grocery"),
    #                 Product("gro_2", "Food Oil", 120, "grocery"),
    #                 Product("gro_3", "Wheat", 26, "grocery"),
    #                 Product("gro_4", "Spices", 10, "grocery"),
    #                 Product("gro_5", "Flour", 30, "grocery"),
    #                 Product("gro_6", "Maggi", 25, "grocery"),
    #                 Product("drk_1", "Sprite", 95, "drinks"),
    #                 Product("drk_2", "Mineral Water", 20, "drinks"),
    #                 Product("drk_3", "Juice", 10, "drinks"),
    #                 Product("drk_4", "Coke", 20, "drinks"),
    #                 Product("drk_5", "Lassi", 30, "drinks"),
    #                 Product("drk_6", "Mountain Duo", 100, "drinks")
    #             ]
    #             for product in default_products:
    #                 self.repo.save(product)
    #             print("Default products initialized in Firestore.")
    #     except Exception as e:
    #         print(f"[initialize_default_products] Error initializing default products: {e}")
