"""Face similarity utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

import cv2
import numpy as np


def _histogram(path: str) -> np.ndarray:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None  # type: ignore[return-value]
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    cv2.normalize(hist, hist)
    return hist


def filter_by_similarity(paths: Iterable[str], reference: str, threshold: float = 0.6) -> List[str]:
    """Filter faces by similarity to a reference face."""
    ref_hist = _histogram(reference)
    if ref_hist is None:
        return []
    selected = []
    for p in paths:
        hist = _histogram(p)
        if hist is None:
            continue
        score = cv2.compareHist(ref_hist, hist, cv2.HISTCMP_CORREL)
        if score >= threshold:
            selected.append(p)
        else:
            Path(p).unlink(missing_ok=True)
    return selected
