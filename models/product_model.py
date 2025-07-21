class Product:
    """
    Represents a product item in the billing system.

    Attributes:
        product_id (str): Unique identifier for the product.
        name (str): Name of the product.
        price (float): Price of the product.
        category (str): Category to which the product belongs (e.g., medical, grocery, drinks).
    """

    def __init__(self, product_id: str, name: str, price: float, category: str):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category

    def to_dict(self) -> dict:
        """
        Serializes the Product object into a dictionary format.

        Returns:
            dict: Dictionary representation of the product.
        """
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "category": self.category
        }

    @staticmethod
    def from_dict(source: dict) -> 'Product':
        """
        Creates a Product instance from a dictionary.

        Args:
            source (dict): Dictionary representation of a product.

        Returns:
            Product: The reconstructed Product object.

        Raises:
            ValueError: If the source dictionary is malformed.
        """
        try:
            return Product(
                product_id=source.get("product_id", ""),
                name=source.get("name", ""),
                price=source.get("price", 0.0),
                category=source.get("category", "")
            )
        except Exception as e:
            raise ValueError(f"Failed to parse Product from dict: {e}")
