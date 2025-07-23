import customtkinter as ctk

from auth.firebase_auth import FirebaseAuth
from config import icon_path
from ui.billing_window import BillingWindow
from ui.login_window import LoginWindow
from ui.signup_window import SignupWindow


class MainApp:
    def __init__(self):
        self.root = ctk.CTk()
        # Set Appearance and Theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root.iconbitmap(icon_path)

        self.auth = FirebaseAuth()
        self.current_window = None
        self.show_login_window()

    def show_login_window(self):
        self.clear_window()
        self.current_window = LoginWindow(
            root=self.root,
            auth=self.auth,
            login_callback=self.on_login_success,
            signup_callback=self.show_signup_window
        )
        self.current_window.load_login_state()

    def show_signup_window(self):
        self.clear_window()
        self.current_window = SignupWindow(
            root=self.root,
            auth=self.auth,
            back_to_login_callback=self.show_login_window
        )

    def on_login_success(self, user_data):
        # For now, just show a confirmation and close the window.
        from tkinter import messagebox
        messagebox.showinfo("Welcome", f"Logged in as {user_data['email']}")
        self.clear_window()
        self.current_window = BillingWindow(
            root=self.root,
            user_data=user_data
        )

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    MainApp().run()
