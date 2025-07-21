from datetime import datetime
from typing import List, Optional


class BillItem:
    """
    Represents a single item in a bill.

    Attributes:
        product_id (str): Unique identifier for the product.
        product_name (str): Name of the product.
        quantity (int): Quantity of the product purchased.
        price (float): Price per unit of the product.
        total (float): Total cost for the item (quantity * price).
    """

    def __init__(self, product_id: str, product_name: str, quantity: int, price: float, total: float):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
        self.total = total

    def to_dict(self) -> dict:
        """Serializes the BillItem object to a dictionary."""
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "price": self.price,
            "total": self.total
        }

    @staticmethod
    def from_dict(source: dict) -> 'BillItem':
        """
        Creates a BillItem instance from a dictionary.

        Args:
            source (dict): Dictionary representation of a BillItem.

        Returns:
            BillItem: The reconstructed BillItem object.
        """
        return BillItem(
            product_id=source.get("product_id", ""),
            product_name=source.get("product_name", ""),
            quantity=source.get("quantity", 0),
            price=source.get("price", 0.0),
            total=source.get("total", 0.0)
        )


class Bill:
    """
    Represents a full customer bill with multiple categories and tax calculations.

    Attributes:
        bill_no (str): Unique bill number.
        customer_name (str): Name of the customer.
        customer_phone (str): Phone number of the customer.
        items (List[BillItem]): List of billed items.
        medical_total, grocery_total, drinks_total (float): Totals for each category.
        medical_tax, grocery_tax, drinks_tax (float): Tax amounts per category.
        total_amount (float): Grand total of the bill.
        timestamp (datetime): Date and time when the bill was created.
    """

    def __init__(
            self,
            bill_no: str,
            customer_name: str,
            customer_phone: str,
            items: Optional[List[BillItem]] = None,
            medical_total: float = 0.0,
            grocery_total: float = 0.0,
            drinks_total: float = 0.0,
            medical_tax: float = 0.0,
            grocery_tax: float = 0.0,
            drinks_tax: float = 0.0,
            total_amount: float = 0.0,
            timestamp: Optional[datetime] = None
    ):
        self.bill_no = bill_no
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.items = items or []
        self.medical_total = medical_total
        self.grocery_total = grocery_total
        self.drinks_total = drinks_total
        self.medical_tax = medical_tax
        self.grocery_tax = grocery_tax
        self.drinks_tax = drinks_tax
        self.total_amount = total_amount
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> dict:
        """Serializes the Bill object to a dictionary format suitable for Firestore or JSON."""
        return {
            "bill_no": self.bill_no,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "items": [item.to_dict() for item in self.items],
            "medical_total": self.medical_total,
            "grocery_total": self.grocery_total,
            "drinks_total": self.drinks_total,
            "medical_tax": self.medical_tax,
            "grocery_tax": self.grocery_tax,
            "drinks_tax": self.drinks_tax,
            "total_amount": self.total_amount,
            "timestamp": self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(source: dict) -> 'Bill':
        """
        Creates a Bill instance from a dictionary.

        Args:
            source (dict): Dictionary representation of a Bill.

        Returns:
            Bill: The reconstructed Bill object.
        """
        try:
            items = [BillItem.from_dict(item) for item in source.get("items", [])]
            timestamp = source.get("timestamp")
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp)

            return Bill(
                bill_no=source.get("bill_no", ""),
                customer_name=source.get("customer_name", ""),
                customer_phone=source.get("customer_phone", ""),
                items=items,
                medical_total=source.get("medical_total", 0.0),
                grocery_total=source.get("grocery_total", 0.0),
                drinks_total=source.get("drinks_total", 0.0),
                medical_tax=source.get("medical_tax", 0.0),
                grocery_tax=source.get("grocery_tax", 0.0),
                drinks_tax=source.get("drinks_tax", 0.0),
                total_amount=source.get("total_amount", 0.0),
                timestamp=timestamp
            )
        except Exception as e:
            raise ValueError(f"Failed to parse Bill from dict: {e}")
