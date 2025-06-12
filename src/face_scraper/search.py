"""Image search utilities for Fandom."""

from __future__ import annotations

import json
import re
from typing import List

import requests


_STRIP_REVISION_RE = re.compile(r"/revision.*$")


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


def fetch_image_urls(name: str) -> List[str]:
    """Fetch image URLs for ``name`` from multiple sources."""

    fandom = fetch_fandom_image_urls(name)
    return fandom
