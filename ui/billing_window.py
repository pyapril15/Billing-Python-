# Main Application
import random
from datetime import datetime
from tkinter import messagebox as mb

import customtkinter as ctk

from models.bill_model import BillItem, Bill
from services.bill_service import BillService
from services.product_service import ProductService
from services.user_service import UserService
from templates.bill_template import BillPreviewWindow


class BillingWindow:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        self.root.geometry("1400x800+0+0")

        # Configure grid weights for better resizing
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.bill_service = BillService()
        self.user_service = UserService()
        self.product_service = ProductService()
        # self.product_service.initialize_default_products()

        self.user_profile = self.user_service.get_user_profile(self.user_data['localId'])
        self.root.title(f"Billing System - User => {self.user_profile['name'].capitalize()}")

        # Variables
        self.bill_no = ctk.StringVar(value=self.generate_bill_number())
        self.c_name = ctk.StringVar()
        self.c_phone = ctk.StringVar()
        self.search_bill = ctk.StringVar()

        # Category totals and tax variables
        self.medical_price = ctk.StringVar(value="\u20B90.00")
        self.grocery_price = ctk.StringVar(value="\u20B90.00")
        self.cold_drinks_price = ctk.StringVar(value="\u20B90.00")
        self.medical_tax = ctk.StringVar(value="\u20B90.00")
        self.grocery_tax = ctk.StringVar(value="\u20B90.00")
        self.cold_drinks_tax = ctk.StringVar(value="\u20B90.00")

        # Product quantities (for each product)
        self.product_vars = {}

        # Store totals for calculations
        self.total_medical = 0
        self.total_grocery = 0
        self.total_drinks = 0
        self.tax_medical = 0
        self.tax_grocery = 0
        self.tax_drinks = 0
        self.bill_total = 0

        # Create main container using grid instead of pack
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)  # Products area should expand

        # Create UI components
        self.create_header()
        self.create_customer_details()
        self.create_products_area()
        self.create_totals_area()
        self.create_action_buttons()

        # Load products from Firestore
        self.load_products()

    @staticmethod
    def generate_bill_number():
        return str(random.randint(10000, 99999))

    def create_header(self):
        header_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            header_frame,
            text="Modern Billing System",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=20)

    def create_customer_details(self):
        customer_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        customer_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        # Configure grid columns
        for i in range(7):
            customer_frame.grid_columnconfigure(i, weight=1)

        # Header
        ctk.CTkLabel(
            customer_frame,
            text="Customer Details",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=6, pady=10, padx=10, sticky="w")

        # Customer Name
        ctk.CTkLabel(
            customer_frame,
            text="Customer Name:",
            font=ctk.CTkFont(size=14)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")

        name_entry = ctk.CTkEntry(
            customer_frame,
            textvariable=self.c_name,
            width=200,
            height=30,
            font=ctk.CTkFont(size=14)
        )
        name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Customer Phone
        ctk.CTkLabel(
            customer_frame,
            text="Phone Number:",
            font=ctk.CTkFont(size=14)
        ).grid(row=1, column=2, padx=10, pady=10, sticky="w")

        phone_entry = ctk.CTkEntry(
            customer_frame,
            textvariable=self.c_phone,
            width=200,
            height=30,
            font=ctk.CTkFont(size=14)
        )
        phone_entry.grid(row=1, column=3, padx=10, pady=10, sticky="ew")

        # Bill Number
        ctk.CTkLabel(
            customer_frame,
            text="Bill Number:",
            font=ctk.CTkFont(size=14)
        ).grid(row=1, column=4, padx=10, pady=10, sticky="w")

        bill_entry = ctk.CTkEntry(
            customer_frame,
            textvariable=self.search_bill,
            width=200,
            height=30,
            font=ctk.CTkFont(size=14)
        )
        bill_entry.grid(row=1, column=5, padx=10, pady=10, sticky="ew")

        # Search Button
        search_btn = ctk.CTkButton(
            customer_frame,
            text="Search",
            command=self.search_bill_cmd,
            width=100,
            height=30,
            font=ctk.CTkFont(size=14)
        )
        search_btn.grid(row=1, column=6, padx=10, pady=10, sticky="ew")

    def create_products_area(self):
        products_frame = ctk.CTkFrame(self.main_frame)
        products_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        products_frame.grid_columnconfigure(0, weight=1)
        products_frame.grid_rowconfigure(0, weight=1)

        # Create notebook with tabs for each category
        tab_view = ctk.CTkTabview(products_frame)
        tab_view.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Configure tab view to expand
        tab_view.grid_columnconfigure(0, weight=1)
        tab_view.grid_rowconfigure(0, weight=1)

        # Create tabs for each product category
        medical_tab = tab_view.add("Medical Items")
        grocery_tab = tab_view.add("Grocery Items")
        drinks_tab = tab_view.add("Cold Drinks")

        # Configure tab columns and rows
        for tab in [medical_tab, grocery_tab, drinks_tab]:
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)

        # Tab containers for products
        self.medical_items_frame = ctk.CTkScrollableFrame(medical_tab)
        self.medical_items_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.medical_items_frame.grid_columnconfigure(0, weight=3)
        self.medical_items_frame.grid_columnconfigure(1, weight=1)
        self.medical_items_frame.grid_columnconfigure(2, weight=1)

        self.grocery_items_frame = ctk.CTkScrollableFrame(grocery_tab)
        self.grocery_items_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.grocery_items_frame.grid_columnconfigure(0, weight=3)
        self.grocery_items_frame.grid_columnconfigure(1, weight=1)
        self.grocery_items_frame.grid_columnconfigure(2, weight=1)

        self.drinks_items_frame = ctk.CTkScrollableFrame(drinks_tab)
        self.drinks_items_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.drinks_items_frame.grid_columnconfigure(0, weight=3)
        self.drinks_items_frame.grid_columnconfigure(1, weight=1)
        self.drinks_items_frame.grid_columnconfigure(2, weight=1)

    def load_products(self):
        # Clear existing products
        for widget in self.medical_items_frame.winfo_children():
            widget.destroy()
        for widget in self.grocery_items_frame.winfo_children():
            widget.destroy()
        for widget in self.drinks_items_frame.winfo_children():
            widget.destroy()

        # Get products from Firestore by category
        medical_products = self.product_service.get_products_by_category("medical")
        grocery_products = self.product_service.get_products_by_category("grocery")
        drinks_products = self.product_service.get_products_by_category("drinks")

        # Headers for the products
        self.create_product_headers(self.medical_items_frame)
        self.create_product_headers(self.grocery_items_frame)
        self.create_product_headers(self.drinks_items_frame)

        # Add products to UI
        self.add_products_to_frame(medical_products, self.medical_items_frame, start_row=1)
        self.add_products_to_frame(grocery_products, self.grocery_items_frame, start_row=1)
        self.add_products_to_frame(drinks_products, self.drinks_items_frame, start_row=1)

    @staticmethod
    def create_product_headers(frame):
        """Create headers for product lists"""
        # Product name header
        header_label = ctk.CTkLabel(
            frame,
            text="Product Name",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        header_label.grid(row=0, column=0, padx=10, pady=(5, 10), sticky="w")

        # Price header
        price_header = ctk.CTkLabel(
            frame,
            text="Price",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        price_header.grid(row=0, column=1, padx=10, pady=(5, 10))

        # Quantity header
        qty_header = ctk.CTkLabel(
            frame,
            text="Quantity",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        qty_header.grid(row=0, column=2, padx=10, pady=(5, 10))

        # Actions header
        actions_header = ctk.CTkLabel(
            frame,
            text="Actions",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        actions_header.grid(row=0, column=3, columnspan=2, padx=10, pady=(5, 10))

    def add_products_to_frame(self, products, frame, start_row=0):
        row = start_row
        for product in products:
            # Create variable for this product
            self.product_vars[product.product_id] = ctk.IntVar(value=0)

            # Product name label
            product_label = ctk.CTkLabel(
                frame,
                text=product.name,
                font=ctk.CTkFont(size=14)
            )
            product_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

            # Price label
            price_label = ctk.CTkLabel(
                frame,
                text=f"\u20B9{product.price:.2f}",
                font=ctk.CTkFont(size=14)
            )
            price_label.grid(row=row, column=1, padx=10, pady=5)

            # Quantity entry
            qty_entry = ctk.CTkEntry(
                frame,
                textvariable=self.product_vars[product.product_id],
                width=70,
                height=30,
                font=ctk.CTkFont(size=14)
            )
            qty_entry.grid(row=row, column=2, padx=10, pady=5)

            # Create a frame for buttons
            btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
            btn_frame.grid(row=row, column=3, columnspan=2, padx=10, pady=5)

            # Add/Remove buttons
            remove_btn = ctk.CTkButton(
                btn_frame,
                text="-",
                width=30,
                height=30,
                command=lambda p=product.product_id: self.decrease_quantity(p)
            )
            remove_btn.pack(side="left", padx=2)

            add_btn = ctk.CTkButton(
                btn_frame,
                text="+",
                width=30,
                height=30,
                command=lambda p=product.product_id: self.increase_quantity(p)
            )
            add_btn.pack(side="left", padx=2)

            row += 1

    def increase_quantity(self, product_id):
        current_value = self.product_vars[product_id].get()
        self.product_vars[product_id].set(current_value + 1)
        # Auto-calculate totals when quantity changes
        self.calculate_total()

    def decrease_quantity(self, product_id):
        current_value = self.product_vars[product_id].get()
        if current_value > 0:
            self.product_vars[product_id].set(current_value - 1)
            # Auto-calculate totals when quantity changes
            self.calculate_total()

    def create_totals_area(self):
        totals_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        totals_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

        # Configure columns
        for i in range(4):
            totals_frame.grid_columnconfigure(i, weight=1)

        # Category totals header
        ctk.CTkLabel(
            totals_frame,
            text="Category Totals",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="w")

        # Medical totals
        ctk.CTkLabel(
            totals_frame,
            text="Medical Total:",
            font=ctk.CTkFont(size=14)
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(
            totals_frame,
            textvariable=self.medical_price,
            width=120,
            height=30,
            font=ctk.CTkFont(size=14),
            anchor="w"
        ).grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Medical tax
        ctk.CTkLabel(
            totals_frame,
            text="Medical Tax:",
            font=ctk.CTkFont(size=14)
        ).grid(row=1, column=2, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(
            totals_frame,
            textvariable=self.medical_tax,
            width=120,
            height=30,
            font=ctk.CTkFont(size=14),
            anchor="w"
        ).grid(row=1, column=3, padx=10, pady=5, sticky="w")

        # Grocery totals
        ctk.CTkLabel(
            totals_frame,
            text="Grocery Total:",
            font=ctk.CTkFont(size=14)
        ).grid(row=2, column=0, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(
            totals_frame,
            textvariable=self.grocery_price,
            width=120,
            height=30,
            font=ctk.CTkFont(size=14),
            anchor="w"
        ).grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Grocery tax
        ctk.CTkLabel(
            totals_frame,
            text="Grocery Tax:",
            font=ctk.CTkFont(size=14)
        ).grid(row=2, column=2, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(
            totals_frame,
            textvariable=self.grocery_tax,
            width=120,
            height=30,
            font=ctk.CTkFont(size=14),
            anchor="w"
        ).grid(row=2, column=3, padx=10, pady=5, sticky="w")

        # Cold drinks totals
        ctk.CTkLabel(
            totals_frame,
            text="Drinks Total:",
            font=ctk.CTkFont(size=14)
        ).grid(row=3, column=0, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(
            totals_frame,
            textvariable=self.cold_drinks_price,
            width=120,
            height=30,
            font=ctk.CTkFont(size=14),
            anchor="w"
        ).grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Cold drinks tax
        ctk.CTkLabel(
            totals_frame,
            text="Drinks Tax:",
            font=ctk.CTkFont(size=14)
        ).grid(row=3, column=2, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(
            totals_frame,
            textvariable=self.cold_drinks_tax,
            width=120,
            height=30,
            font=ctk.CTkFont(size=14),
            anchor="w"
        ).grid(row=3, column=3, padx=10, pady=5, sticky="w")

        # Grand total
        ctk.CTkLabel(
            totals_frame,
            text="Grand Total:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.grand_total_label = ctk.CTkLabel(
            totals_frame,
            text="\u20B90.00",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.grand_total_label.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    def create_action_buttons(self):
        buttons_frame = ctk.CTkFrame(self.main_frame)
        buttons_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=10)

        # Configure grid columns for better button spacing
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)

        # Total button
        total_btn = ctk.CTkButton(
            buttons_frame,
            text="Calculate Total",
            command=self.calculate_total,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        total_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Generate Bill button
        gen_bill_btn = ctk.CTkButton(
            buttons_frame,
            text="Generate Bill",
            command=self.show_bill_preview,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        gen_bill_btn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Clear button
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="Clear",
            command=self.clear_fields,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        clear_btn.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Exit button
        exit_btn = ctk.CTkButton(
            buttons_frame,
            text="Exit",
            command=self.exit_app,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        exit_btn.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

    def calculate_total(self):
        """Calculate totals for all categories and update the UI"""
        # Get all products from Firestore
        all_products = {p.product_id: p for p in self.product_service.get_all_products()}

        # Calculate category totals
        medical_total = 0
        grocery_total = 0
        drinks_total = 0

        # Iterate through product variables to calculate totals
        for product_id, var in self.product_vars.items():
            quantity = var.get()
            if quantity > 0 and product_id in all_products:
                product = all_products[product_id]
                item_total = quantity * product.price

                if product.category == "medical":
                    medical_total += item_total
                elif product.category == "grocery":
                    grocery_total += item_total
                elif product.category == "drinks":
                    drinks_total += item_total

        # Calculate taxes
        medical_tax = round(medical_total * 0.05, 2)
        grocery_tax = round(grocery_total * 0.01, 2)
        drinks_tax = round(drinks_total * 0.10, 2)

        # Calculate grand total
        grand_total = medical_total + grocery_total + drinks_total + medical_tax + grocery_tax + drinks_tax

        # Update UI variables
        self.medical_price.set(f"\u20B9{medical_total:.2f}")
        self.grocery_price.set(f"\u20B9{grocery_total:.2f}")
        self.cold_drinks_price.set(f"\u20B9{drinks_total:.2f}")

        self.medical_tax.set(f"\u20B9{medical_tax:.2f}")
        self.grocery_tax.set(f"\u20B9{grocery_tax:.2f}")
        self.cold_drinks_tax.set(f"\u20B9{drinks_tax:.2f}")

        # Update grand total
        self.grand_total_label.configure(text=f"\u20B9{grand_total:.2f}")

        # Store calculated values for later use
        self.total_medical = medical_total
        self.total_grocery = grocery_total
        self.total_drinks = drinks_total
        self.tax_medical = medical_tax
        self.tax_grocery = grocery_tax
        self.tax_drinks = drinks_tax
        self.bill_total = grand_total

    def prepare_bill_data(self):
        """Prepare bill data for generating PDF"""
        # Get all products from service
        all_products = {p.product_id: p for p in self.product_service.get_all_products()}

        # Create list of bill items
        bill_items = []
        for product_id, var in self.product_vars.items():
            quantity = var.get()
            if quantity > 0 and product_id in all_products:
                product = all_products[product_id]
                total = quantity * product.price

                bill_items.append(BillItem(
                    product_id=product_id,
                    product_name=product.name,
                    price=product.price,
                    quantity=quantity,
                    total=total
                ))

        # Create and return bill data
        return Bill(
            bill_no=self.bill_no.get(),
            customer_name=self.c_name.get(),
            customer_phone=self.c_phone.get(),
            items=bill_items,
            medical_total=self.total_medical,
            grocery_total=self.total_grocery,
            drinks_total=self.total_drinks,
            medical_tax=self.tax_medical,
            grocery_tax=self.tax_grocery,
            drinks_tax=self.tax_drinks,
            total_amount=self.bill_total,
            timestamp=datetime.now()
        )

    def show_bill_preview(self):
        """Show bill preview window"""
        # Check if customer details are filled
        if not self.c_name.get() or not self.c_phone.get():
            mb.showerror("Error", "Customer details are required")
            return

        # Check if any products are selected
        any_products = False
        for var in self.product_vars.values():
            if var.get() > 0:
                any_products = True
                break

        if not any_products:
            mb.showerror("Error", "No products selected")
            return

        # Calculate total if not already done
        self.calculate_total()

        # Create bill data
        bill_data = self.prepare_bill_data()

        # Save bill to database
        self.bill_service.create_bill(bill_data)

        # Show bill preview
        BillPreviewWindow(self.root, bill_data, self.user_profile)

        # Reset fields for next bill
        self.bill_no.set(self.generate_bill_number())

    def search_bill_cmd(self):
        """Search for existing bill and populate fields if found"""
        bill_number = self.search_bill.get()
        if not bill_number:
            mb.showerror("Error", "Please enter bill number to search")
            return

        # Get bill from database
        bill_data = self.bill_service.get_bill(bill_number)

        if bill_data:
            # Show bill preview
            BillPreviewWindow(self.root, bill_data, self.user_profile)

            # Populate fields with bill data
            self.populate_fields_with_bill(bill_data)
        else:
            mb.showerror("Error", "Bill not found")

    def populate_fields_with_bill(self, bill_data):
        """Populate all fields with data from found bill"""
        # Clear existing fields first
        self.clear_fields()

        # Set bill number and customer details
        self.bill_no.set(bill_data.bill_no)
        self.c_name.set(bill_data.customer_name)
        self.c_phone.set(bill_data.customer_phone)

        # Set quantities for products in the bill
        for item in bill_data.items:
            if item.product_id in self.product_vars:
                self.product_vars[item.product_id].set(item.quantity)

        # Update totals
        self.total_medical = bill_data.medical_total
        self.total_grocery = bill_data.grocery_total
        self.total_drinks = bill_data.drinks_total
        self.tax_medical = bill_data.medical_tax
        self.tax_grocery = bill_data.grocery_tax
        self.tax_drinks = bill_data.drinks_tax
        self.bill_total = bill_data.total_amount

        # Update UI
        self.medical_price.set(f"\u20B9{self.total_medical:.2f}")
        self.grocery_price.set(f"\u20B9{self.total_grocery:.2f}")
        self.cold_drinks_price.set(f"\u20B9{self.total_drinks:.2f}")
        self.medical_tax.set(f"\u20B9{self.tax_medical:.2f}")
        self.grocery_tax.set(f"\u20B9{self.tax_grocery:.2f}")
        self.cold_drinks_tax.set(f"\u20B9{self.tax_drinks:.2f}")
        self.grand_total_label.configure(text=f"\u20B9{self.bill_total:.2f}")

        mb.showinfo("Bill Found", f"Bill #{bill_data.bill_no} has been loaded")

    def clear_fields(self):
        """Clear all fields"""
        # Clear customer info
        self.c_name.set("")
        self.c_phone.set("")
        self.search_bill.set("")

        # Clear product quantities
        for var in self.product_vars.values():
            var.set(0)

        # Clear totals
        self.medical_price.set("\u20B90.00")
        self.grocery_price.set("\u20B90.00")
        self.cold_drinks_price.set("\u20B90.00")
        self.medical_tax.set("\u20B90.00")
        self.grocery_tax.set("\u20B90.00")
        self.cold_drinks_tax.set("\u20B90.00")
        self.grand_total_label.configure(text="\u20B90.00")

        # Reset stored values
        self.total_medical = 0
        self.total_grocery = 0
        self.total_drinks = 0
        self.tax_medical = 0
        self.tax_grocery = 0
        self.tax_drinks = 0
        self.bill_total = 0

        # Generate new bill number
        self.bill_no.set(self.generate_bill_number())

    def exit_app(self):
        """Exit application"""
        if mb.askyesno("Exit", "Do you want to exit?"):
            self.root.destroy()
