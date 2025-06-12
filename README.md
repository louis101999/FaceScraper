# Face Scraper

A tool to fetch celebrity images from multiple sources, filter them for quality, extract faces, and keep only those matching the target person.

## Usage

```bash
pip install -e .
face-scraper "Celebrity Name" --output ./data
```

Currently images are sourced from:

- [Fandom](https://www.fandom.com/) wikis via the hidden Lightbox endpoint
- [Pinterest](https://www.pinterest.com/) using the `pinscrape` library's
  ``scraper.scrape`` helper

Additional sources can be added by creating new search functions and registering them in ``face_scraper.search.SOURCES``.
