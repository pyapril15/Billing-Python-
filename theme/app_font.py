# theme/app_font.py

import customtkinter as ctk

def get_fonts():
    return {
        "FONT_TITLE": ctk.CTkFont(size=24, weight="bold"),
        "FONT_SUBTITLE": ctk.CTkFont(size=14),
        "FONT_INPUT": ctk.CTkFont(size=13),
        "FONT_BUTTON": ctk.CTkFont(size=14, weight="bold")
    }
