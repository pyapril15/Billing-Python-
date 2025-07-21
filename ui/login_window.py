import os
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage

from auth.firebase_config import FirebaseConfig
from config import login_cache_path
from services.asset_service import AssetService
from theme.app_font import get_fonts


class LoginWindow:
    def __init__(self, root, auth, login_callback, signup_callback):
        self.root = root
        self.auth = auth
        self.login_callback = login_callback
        self.signup_callback = signup_callback

        firebase_config = FirebaseConfig()
        asset_service = AssetService(firebase_config.db)

        self.fonts = get_fonts()
        self.show_password = ctk.BooleanVar(value=False)
        self.remember_var = ctk.BooleanVar(value=False)

        self.root.title("Login - Billing System")

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

            asset_info = asset_service.get_asset_info("login", "bg_image")
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

        # ===== Container =====
        self.container = ctk.CTkFrame(self.right_frame, fg_color="#fff", corner_radius=12)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.inner_frame = ctk.CTkFrame(self.container, fg_color="transparent", corner_radius=0)
        self.inner_frame.pack(padx=30, pady=30, fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(self.inner_frame, text="Welcome Back", font=self.fonts["FONT_TITLE"])
        self.title_label.pack(pady=(0, 10))

        self.subtitle_label = ctk.CTkLabel(
            self.inner_frame,
            text="Log in to access your account",
            font=self.fonts["FONT_SUBTITLE"],
            text_color="#7a7a7a",
        )
        self.subtitle_label.pack(pady=(0, 20))

        # Email Entry
        self.email_entry = ctk.CTkEntry(self.inner_frame, placeholder_text="Email", width=240,
                                        font=self.fonts["FONT_INPUT"])
        self.email_entry.pack(pady=10)

        # Password Frame with Toggle
        self.password_frame = ctk.CTkFrame(self.inner_frame, fg_color="transparent")
        self.password_frame.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.password_frame, placeholder_text="Password", show="*", width=200,
                                           font=self.fonts["FONT_INPUT"])
        self.password_entry.pack(side="left", padx=(0, 10))

        self.toggle_button = ctk.CTkButton(self.password_frame, text="\U0001F441", width=30,
                                           command=self.toggle_password_visibility)
        self.toggle_button.pack(side="left")

        # Remember Me and Forgot Password
        self.options_frame = ctk.CTkFrame(self.inner_frame, fg_color="transparent")
        self.options_frame.pack(fill='x', pady=(5, 15), padx=5)

        self.remember_me_checkbox = ctk.CTkCheckBox(
            self.options_frame, text="Remember Me",
            variable=self.remember_var,
            checkbox_height=14, checkbox_width=14,
            font=self.fonts["FONT_INPUT"]
        )
        self.remember_me_checkbox.pack(side="left")

        self.forgot_button = ctk.CTkButton(
            self.options_frame, text="Forgot Password?", fg_color="transparent",
            text_color="blue", hover_color="#fff", font=self.fonts["FONT_INPUT"],
            command=self.forgot_password, width=130
        )
        self.forgot_button.pack(side="right")

        # Login Button
        self.login_button = ctk.CTkButton(
            self.inner_frame,
            text="Login",
            font=self.fonts["FONT_BUTTON"],
            fg_color="#3478f6",
            hover_color="#2257c1",
            command=self.login
        )
        self.login_button.pack(fill='x', pady=(10, 10), padx=5)

        # Sign Up Button
        self.signup_button = ctk.CTkButton(
            self.inner_frame,
            text="Sign Up",
            font=self.fonts["FONT_INPUT"],
            fg_color="transparent",
            text_color="blue",
            hover_color="#d0e4ff",
            command=self.signup
        )
        self.signup_button.pack(fill='x', pady=(0, 5), padx=5)

    def toggle_password_visibility(self):
        if self.show_password.get():
            self.password_entry.configure(show="*")
            self.toggle_button.configure(text="\U0001F441")
            self.show_password.set(False)
        else:
            self.password_entry.configure(show="")
            self.toggle_button.configure(text="\U0001F648")
            self.show_password.set(True)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email:
            self.show_validation_error("Email is required")
            self.email_entry.focus_set()
            return

        if not password:
            self.show_validation_error("Password is required")
            self.password_entry.focus_set()
            return

        try:
            self.root.config(cursor="wait")
            self.root.update()

            user = self.auth.sign_in(email, password)
            user_info = self.auth.auth.get_account_info(user["idToken"])
            is_verified = user_info["users"][0].get("emailVerified", False)
            uid = user_info["users"][0]["localId"]

            if not is_verified:
                self.root.config(cursor="")
                resend = messagebox.askyesno("Email Not Verified",
                                             "Your email is not verified. Resend verification email?")
                if resend:
                    self.auth.send_email_verification(user["idToken"])
                    messagebox.showinfo("Verification Sent", "A new verification email has been sent.")
                self.auth.sign_out()
                return

            from services.user_service import UserService
            user_service = UserService()
            user_service.update_email_verification(uid, True)

            if self.remember_var:
                self.save_login_state(email)

            self.root.config(cursor="")
            messagebox.showinfo("Login Success", f"Welcome {email}!")
            self.login_callback(user)

        except Exception as e:
            self.root.config(cursor="")
            messagebox.showerror("Login Failed", str(e))

    @staticmethod
    def show_validation_error(message):
        messagebox.showerror("Validation Error", message)

    def signup(self):
        self.signup_callback()

    def forgot_password(self):
        email = self.email_entry.get().strip()

        if not email:
            self.show_validation_error("Enter your email to reset password")
            self.email_entry.focus_set()
            return

        try:
            self.root.config(cursor="wait")
            self.root.update()
            self.auth.reset_password(email)
            self.root.config(cursor="")
            messagebox.showinfo("Reset Email Sent", "Check your email for reset instructions.")
        except Exception as e:
            self.root.config(cursor="")
            messagebox.showerror("Reset Failed", str(e))

    @staticmethod
    def save_login_state(email):
        try:
            cache_file = os.path.join(login_cache_path(), ".login_cache")
            with open(cache_file, "w") as f:
                f.write(email)
        except Exception as e:
            print(f"Failed to save login state: {e}")

    def load_login_state(self):
        try:
            cache_file = os.path.join(login_cache_path(), ".login_cache")
            if os.path.exists(cache_file):
                with open(cache_file, "r") as f:
                    email = f.read().strip()
                    if email:
                        self.email_entry.insert(0, email)
                        self.remember_var.set(True)
        except Exception as e:
            print(f"Failed to load login state: {e}")
