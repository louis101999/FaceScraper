"""Image quality assessment."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

import cv2


MIN_RESOLUTION = (256, 256)
BLUR_THRESHOLD = 100.0


def _is_high_resolution(image_path: str) -> bool:
    img = cv2.imread(image_path)
    if img is None:
        return False
    h, w = img.shape[:2]
    return w >= MIN_RESOLUTION[0] and h >= MIN_RESOLUTION[1]


def _is_sharp(image_path: str) -> bool:
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return False
    variance = cv2.Laplacian(img, cv2.CV_64F).var()
    return variance >= BLUR_THRESHOLD


def filter_images(paths: Iterable[str]) -> List[str]:
    """Filter images that meet quality criteria."""
    good_paths = []
    for p in paths:
        if _is_high_resolution(p) and _is_sharp(p):
            good_paths.append(p)
        else:
            Path(p).unlink(missing_ok=True)
    return good_paths
