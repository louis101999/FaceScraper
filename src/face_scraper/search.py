"""Image search utilities for multiple sources.

This module currently supports Fandom and Pinterest. Each source provides a
function that returns a list of image URLs. New sources can be added by
implementing additional functions and registering them in ``SOURCES``.
"""

from __future__ import annotations

import json
import re
from typing import Callable, Iterable, List

import requests
from pinscrape import Pinterest


_STRIP_REVISION_RE = re.compile(r"/revision.*$")

# Type alias for a search function
SearchFunc = Callable[[str, int], List[str]]


def fetch_fandom_image_urls(name: str) -> List[str]:
    """Return image URLs from ``<name>.fandom.com`` using the Lightbox endpoint.

    This function performs a simple slug transformation on ``name`` to guess the
    Fandom subdomain. It then iterates over Lightbox batches until no more
    images are returned.
    """

    sub = re.sub(r"[^a-z0-9]", "", name.lower())
    base = f"https://{sub}.fandom.com"
    images: List[str] = []
    batch = 0
    headers = {"User-Agent": "Mozilla/5.0"}

    while True:
        url = (
            f"{base}/wikia.php?controller=Lightbox&method=getFilteredThumbImages"
            f"&batchNum={batch}&count=10000&format=json&inclusive=true"
        )
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            break
        data = resp.json()
        batch_items = []
        for item in data.get("items", []):
            raw = item.get("url") or item.get("thumbUrl")
            if raw:
                full = _STRIP_REVISION_RE.sub("", raw)
                batch_items.append(full)
        if not batch_items:
            break
        images.extend(batch_items)
        batch += 1
    return images


def fetch_pinterest_image_urls(keyword: str, limit: int = 50) -> List[str]:
    """Return image URLs from Pinterest using ``pinscrape``."""

    p = Pinterest()
    try:
        return p.search(keyword, limit)
    except Exception:
        return []


SOURCES: List[SearchFunc] = [fetch_fandom_image_urls, fetch_pinterest_image_urls]


async def fetch_image_urls_async(name: str, limit: int = 50) -> List[str]:
    """Asynchronously gather image URLs from all sources."""

    import asyncio

    tasks = [asyncio.to_thread(src, name, limit) for src in SOURCES]
    results = await asyncio.gather(*tasks)
    urls: List[str] = []
    for res in results:
        urls.extend(res)
    return urls


def fetch_image_urls(name: str, limit: int = 50) -> List[str]:
    """Synchronous wrapper around :func:`fetch_image_urls_async`."""

    import asyncio

    return asyncio.run(fetch_image_urls_async(name, limit))
