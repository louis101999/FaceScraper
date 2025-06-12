# Face Scraper

A tool to fetch celebrity images from Fandom wikis and Pinterest, filter them for quality, extract faces, and keep only those matching the target person.

## Usage

```bash
pip install -e .
face-scraper "Celebrity Name" --output ./data
```

Images are sourced from [Fandom](https://www.fandom.com/) and Pinterest via the
[pinscrape](https://pypi.org/project/pinscrape/) package.
