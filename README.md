# Face Scraper

A tool to fetch celebrity images from Fandom wikis, filter them for quality, extract faces, and keep only those matching the target person.

## Usage

```bash
pip install -e .
face-scraper "Celebrity Name" --output ./data
```

Images are sourced from [Fandom](https://www.fandom.com/) wikis using the hidden Lightbox endpoint.
