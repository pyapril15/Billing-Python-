import os
import sys

from platformdirs import user_cache_dir

APP_NAME = "BillingSystem"


def is_frozen() -> bool:
    """
    Check if the application is running in a frozen (compiled) state,
    such as with PyInstaller.

    Returns:
        bool: True if running as a bundled executable, False otherwise.
    """
    return getattr(sys, 'frozen', False)


def base_path() -> str:
    """
    Determine the base path of the application.

    Returns:
        str: Base directory for the application, adjusted for frozen or script mode.
    """
    try:
        if is_frozen():
            return os.path.join(user_cache_dir(APP_NAME))
        return os.path.dirname(os.path.abspath(__file__))
    except Exception as e:
        raise RuntimeError(f"Failed to determine base path: {e}")


def ensure_dir(path: str) -> str:
    """
    Ensure that a directory exists at the given path.

    Args:
        path (str): Directory path to ensure.

    Returns:
        str: The same directory path, once ensured.
    """
    try:
        os.makedirs(path, exist_ok=True)
        return path
    except Exception as e:
        raise RuntimeError(f"Failed to create or access directory '{path}': {e}")


def cache_path() -> str:
    """
    Get the path to the application's root cache directory.

    Returns:
        str: Full path to the cache directory.
    """
    return ensure_dir(os.path.join(base_path(), "cache"))


def assets_cache_path() -> str:
    """
    Get the path to the assets cache directory.

    Returns:
        str: Full path to the assets cache directory.
    """
    return ensure_dir(os.path.join(cache_path(), "assets"))


def login_cache_path() -> str:
    """
    Get the path to the login cache directory.

    Returns:
        str: Full path to the login cache directory.
    """
    return ensure_dir(os.path.join(cache_path(), "login"))


def bills_path() -> str:
    """
    Get the path to the directory where billing data/files should be stored.

    Returns:
        str: Full path to the bill's directory.
    """
    return ensure_dir(os.path.join(base_path(), "bills"))


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller .exe"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Usage
icon_path = resource_path("assets/billing.ico")
service_key_path = resource_path("auth/serviceAccountKey.json")

