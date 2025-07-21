import hashlib
import os
from io import BytesIO
from typing import Optional

import requests
from PIL import Image
from google.cloud.firestore import Client

from config import assets_cache_path


class AssetService:
    """
    Service for managing and caching remote assets (e.g., images) from Firestore.

    Responsibilities:
    - Retrieve asset metadata from Firestore
    - Download assets from URL and cache them locally
    - Load assets from the local cache when available
    """

    def __init__(self, db: Client, cache_dir: str = "cache/assets"):
        """
        Initialize the AssetService.

        Args:
            db (Client): Firestore database client.
            cache_dir (str, optional): Directory path for cached assets. Defaults to "cache/assets".
        """
        try:
            self.cache_dir = assets_cache_path()
            os.makedirs(self.cache_dir, exist_ok=True)
            self.db = db
            self.assets_collection = self.db.collection("assets")
        except Exception as e:
            raise Exception(f"Failed to initialize AssetService: {e}")

    def get_asset_info(self, category: str, key: str) -> Optional[dict]:
        """
        Retrieve asset URL and version from Firestore.

        Args:
            category (str): Firestore document ID under the 'assets' collection.
            key (str): Asset key (e.g., 'logo', 'banner').

        Returns:
            dict: { 'url': <asset_url>, 'version': <version> } or None if not found.
        """
        try:
            doc = self.assets_collection.document(category).get()
            if doc.exists:
                data = doc.to_dict()
                return {
                    "url": data.get(key),
                    "version": data.get(f"{key}_version", "v1")
                }
            return None
        except Exception as e:
            print(f"[AssetService] Error retrieving asset info: {e}")
            return None

    def load_image_from_url(self, url: str, version: str = "v1") -> Optional[Image.Image]:
        """
        Download and cache an image from a URL or load it from local cache if available.

        Args:
            url (str): The URL of the image to load.
            version (str, optional): Version tag for cache differentiation. Defaults to "v1".

        Returns:
            Image.Image: PIL Image object if successful, otherwise None.
        """
        if not url:
            return None

        try:
            # Create a unique cache filename using the URL hash and version
            name_hash = hashlib.md5(url.encode()).hexdigest()
            filename = f"{name_hash}_{version}.png"
            filepath = os.path.join(self.cache_dir, filename)

            # Return cached image if it exists
            if os.path.exists(filepath):
                return Image.open(filepath)

            # Download and cache the image
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            image.save(filepath)
            return image

        except Exception as e:
            print(f"[AssetService] Error loading image from URL: {e}")
            return None
