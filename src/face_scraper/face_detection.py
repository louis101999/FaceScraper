"""Face detection utilities."""

from __future__ import annotations

import cv2
from typing import List


CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"


def detect_and_crop_faces(image_paths: List[str], dest_dir: str) -> List[str]:
    """Detect faces and save cropped images.

    Parameters
    ----------
    image_paths:
        List of image file paths.
    dest_dir:
        Directory where cropped faces will be stored.

    Returns
    -------
    List[str]
        Paths to cropped face images.
    """
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    face_paths: List[str] = []

    for i, path in enumerate(image_paths):
        img = cv2.imread(path)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        for j, (x, y, w, h) in enumerate(faces):
            crop = img[y:y + h, x:x + w]
            face_path = f"{dest_dir}/face_{i}_{j}.jpg"
            cv2.imwrite(face_path, crop)
            face_paths.append(face_path)
    return face_paths
