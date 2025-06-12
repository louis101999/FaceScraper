"""Command-line interface for face-scraper."""
from __future__ import annotations

import argparse
from pathlib import Path

from . import (
    detect_and_crop_faces,
    download_images,
    fetch_image_urls,
    filter_by_similarity,
    filter_images,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Celebrity image scraper")
    parser.add_argument("name", help="Name of the celebrity")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output"),
        help="Directory to store images",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_dir = args.output / "raw"
    faces_dir = args.output / "faces"
    raw_dir.mkdir(parents=True, exist_ok=True)
    faces_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching images for {args.name}...")
    urls = fetch_image_urls(args.name)
    print(f"Found {len(urls)} images. Downloading...")
    image_paths = download_images(urls, str(raw_dir))
    print("Filtering images...")
    filtered_paths = filter_images(image_paths)
    print("Detecting faces...")
    faces = detect_and_crop_faces(filtered_paths, str(faces_dir))
    if faces:
        print("Filtering by similarity...")
        filter_by_similarity(faces, faces[0])
    print("Done.")


if __name__ == "__main__":
    main()
