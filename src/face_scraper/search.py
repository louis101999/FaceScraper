"""Image search utilities."""

from __future__ import annotations

import requests
from typing import List

from duckduckgo_search import DDGImages


API_ENDPOINT = "https://en.wikipedia.org/w/api.php"


def fetch_wikipedia_image_urls(person: str) -> List[str]:
    """Fetch image URLs from a Wikipedia page.

    Parameters
    ----------
    person:
        Name of the public figure to search for.

    Returns
    -------
    List[str]
        List of image URLs associated with the page.
    """
    params = {
        "action": "query",
        "format": "json",
        "prop": "images",
        "titles": person,
    }
    resp = requests.get(API_ENDPOINT, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    pages = data.get("query", {}).get("pages", {})
    image_titles = []
    for page in pages.values():
        images = page.get("images", [])
        for img in images:
            title = img.get("title")
            if title:
                image_titles.append(title)

    image_urls: List[str] = []
    for title in image_titles:
        file_params = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url",
        }
        file_resp = requests.get(API_ENDPOINT, params=file_params, timeout=10)
        file_resp.raise_for_status()
        file_data = file_resp.json()
        file_pages = file_data.get("query", {}).get("pages", {})
        for fp in file_pages.values():
            imageinfo = fp.get("imageinfo", [])
            if imageinfo:
                url = imageinfo[0].get("url")
                if url:
                    image_urls.append(url)
    return image_urls


def fetch_duckduckgo_image_urls(query: str, max_results: int = 20) -> List[str]:
    """Fetch image URLs via DuckDuckGo."""
    ddg = DDGImages()
    results = ddg.images(query, max_results=max_results)
    return [r["image"] for r in results if r.get("image")]


def fetch_image_urls(person: str, max_results: int = 20) -> List[str]:
    """Aggregate image URLs from multiple sources."""
    urls = fetch_wikipedia_image_urls(person)
    urls.extend(fetch_duckduckgo_image_urls(person, max_results=max_results))
    return urls
