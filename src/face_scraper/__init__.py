"""Face Scraper package."""

__all__ = [
    "fetch_image_urls",
    "fetch_fandom_image_urls",
    "download_images",
    "detect_and_crop_faces",
    "filter_images",
    "filter_by_similarity",
]

from .search import fetch_image_urls, fetch_fandom_image_urls
from .download import download_images
from .face_detection import detect_and_crop_faces
from .quality import filter_images
from .recognition import filter_by_similarity

