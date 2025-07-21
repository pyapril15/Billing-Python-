from tkinter import messagebox

import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage

from auth.firebase_config import FirebaseConfig
from services.asset_service import AssetService
from theme.app_font import get_fonts


class SignupWindow:
    def __init__(self, root, auth, back_to_login_callback):
        self.root = root
        self.auth = auth
        self.back_to_login_callback = back_to_login_callback

        firebase_config = FirebaseConfig()
        asset_service = AssetService(firebase_config.db)

        self.fonts = get_fonts()

        self.show_password = ctk.BooleanVar(value=False)

        self.root.title("Create - Billing System")

        width = 800
        height = 450
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.resizable(False, False)

        # ===== Left Frame with Background Image =====
        self.left_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.left_frame.place(relx=0, rely=0, relwidth=0.6, relheight=1)

        try:
            left_width = int(0.6 * width)
            left_height = height

            asset_info = asset_service.get_asset_info("signup", "bg_image")
            if asset_info:
                image = asset_service.load_image_from_url(asset_info["url"], asset_info["version"])
                resized_image = image.resize((left_width, left_height), Image.Resampling.LANCZOS)
                self.bg_image = CTkImage(light_image=resized_image, size=(left_width, left_height))
                self.bg_label = ctk.CTkLabel(self.left_frame, image=self.bg_image, text="")
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading image: {e}")

        # ===== Right Frame =====
        self.right_frame = ctk.CTkFrame(self.root, fg_color="#fff", corner_radius=0)
        self.right_frame.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)

        # ===== Container Frame =====
        self.container = ctk.CTkFrame(self.right_frame, fg_color="#fff", corner_radius=12)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.inner_frame = ctk.CTkFrame(self.container, fg_color="transparent", corner_radius=0)
        self.inner_frame.pack(padx=30, pady=30, fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(self.inner_frame, text="Welcome Back", font=self.fonts["FONT_TITLE"])
        self.title_label.pack(pady=(0, 10))

        self.subtitle_label = ctk.CTkLabel(
            self.inner_frame,
            text="Sign Up to create your account",
            font=self.fonts["FONT_SUBTITLE"],
            text_color="#7a7a7a",
        )
        self.subtitle_label.pack(pady=(0, 20))

        # Name
        self.name_entry = ctk.CTkEntry(self.inner_frame, placeholder_text="Name", width=220,
                                       font=self.fonts["FONT_INPUT"])
        self.name_entry.pack(pady=8)

        # Email
        self.email_entry = ctk.CTkEntry(self.inner_frame, placeholder_text="Email", width=220,
                                        font=self.fonts["FONT_INPUT"])
        self.email_entry.pack(pady=8)

        self.password_entry = ctk.CTkEntry(self.inner_frame,
                                           placeholder_text="Password",
                                           show="*", width=220,
                                           font=self.fonts["FONT_INPUT"])
        self.password_entry.pack(pady=8)

        # Password
        self.cnf_password_frame = ctk.CTkFrame(self.inner_frame, fg_color="transparent")
        self.cnf_password_frame.pack(pady=8)

        self.cnf_password_entry = ctk.CTkEntry(self.cnf_password_frame,
                                               placeholder_text="Confirm Password",
                                               show="*", width=180,
                                               font=self.fonts["FONT_INPUT"])
        self.cnf_password_entry.pack(side="left", padx=(0, 10))

        self.toggle_button = ctk.CTkButton(self.cnf_password_frame, text="\U0001F441", width=25,
                                           command=self.toggle_password_visibility)
        self.toggle_button.pack(side="left")

        # shop_name
        self.shop_name_entry = ctk.CTkEntry(self.inner_frame, placeholder_text="Shop Name", width=220,
                                            font=self.fonts["FONT_INPUT"])
        self.shop_name_entry.pack(pady=8)

        # shop_address
        self.shop_address_entry = ctk.CTkEntry(self.inner_frame, placeholder_text="Shop Address", width=220,
                                               font=self.fonts["FONT_INPUT"])
        self.shop_address_entry.pack(pady=8)

        # Sign Up
        self.signup_button = ctk.CTkButton(
            self.inner_frame,
            text="Sign Up",
            font=self.fonts["FONT_INPUT"],
            fg_color="#3478f6",
            hover_color="#2257c1",
            command=self.signup
        )
        self.signup_button.pack(fill='x', pady=(10, 8))

        # Login Button
        self.login_button = ctk.CTkButton(
            self.inner_frame,
            text="Login",
            font=self.fonts["FONT_BUTTON"],
            fg_color="transparent",
            text_color="blue",
            hover_color="#d0e4ff",
            command=self.back_to_login
        )
        self.login_button.pack(fill='x', pady=(0, 5))

    def toggle_password_visibility(self):
        if self.show_password.get():
            self.password_entry.configure(show="*")
            self.toggle_button.configure(text="\U0001F441")
            self.show_password.set(False)
        else:
            self.password_entry.configure(show="")
            self.toggle_button.configure(text="\U0001F648")
            self.show_password.set(True)

    def signup(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.cnf_password_entry.get().strip()
        shop_name = self.shop_name_entry.get().strip()
        shop_address = self.shop_address_entry.get().strip()

        if not name:
            self.show_validation_error("Name is required")
            self.name_entry.focus_set()
            return

        if not email:
            self.show_validation_error("Email is required")
            self.email_entry.focus_set()
            return

        if not password:
            self.show_validation_error("Password is required")
            self.password_entry.focus_set()
            return

        if not confirm_password:
            self.show_validation_error("Confirm Password is required")
            self.cnf_password_entry.focus_set()
            return

        if not shop_name:
            self.show_validation_error("Shop Name is required")
            self.shop_name_entry.focus_set()
            return

        if not shop_address:
            self.show_validation_error("Shop Address is required")
            self.shop_address_entry.focus_set()
            return

        if password != confirm_password:
            messagebox.showerror("Validation Error", "Passwords do not match.")
            return

        if len(password) < 6:
            messagebox.showerror("Validation Error", "Password must be at least 6 characters.")
            return

        try:
            # 1. Create account in Firebase
            user_data = self.auth.sign_up(email, password)

            # 2. Save user info in Firestore (via user_service)
            from services.user_service import UserService  # Import here to avoid circular import
            user_service = UserService()
            user_info = self.auth.auth.get_account_info(user_data["idToken"])
            user_service.create_user(user_info["users"][0], name, shop_name, shop_address)

            # 4. Feedback and return to log in
            messagebox.showinfo("Verify Your Email",
                                "A verification link has been sent to your email.\nPlease verify before logging in.")
            self.auth.sign_out()
            self.back_to_login_callback()
        except Exception as e:
            messagebox.showerror("Sign Up Failed", str(e))

    def back_to_login(self):
        self.back_to_login_callback()

    @staticmethod
    def show_validation_error(message):
        """Show a validation error message"""
        messagebox.showerror("Validation Error", message)
