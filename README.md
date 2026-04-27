# Building Science Archive

A static archive and searchable browser for [Building Science Corporation](https://buildingscience.com) documents, guides, and digests.

## Directory Structure

```
buildingscience-archive/
├── .github/
│   └── workflows/
│       ├── archive.yml      # Monthly cron – re-scrape & commit
│       └── deploy.yml       # GitHub Pages deploy on push to main
├── archive/                 # Crawled HTML pages & assets (git-ignored)
├── scripts/
│   ├── scrape_buildingscience.py   # Scraper – fetches & saves pages
│   ├── build_browser.py            # Builds index.json from archive
│   ├── index.html                  # Searchable browser UI
│   └── index.json                  # Generated document index
├── .gitignore
└── README.md
```

## How It Works

1. **Scrape** – `scripts/scrape_buildingscience.py` crawls buildingscience.com and saves pages into `archive/`.
2. **Index** – `scripts/build_browser.py` reads the archive and produces `scripts/index.json`.
3. **Browse** – `scripts/index.html` is a self-contained static page (with Fuse.js search) that loads `index.json` and renders the archive.
4. **Automate** – A GitHub Actions workflow (`archive.yml`) runs the scraper monthly and commits any changes.
5. **Publish** – Every push to `main` triggers `deploy.yml`, which deploys the site to GitHub Pages.

## Local Development

```bash
# Install dependencies
pip install requests beautifulsoup4 lxml

# Run the scraper
python scripts/scrape_buildingscience.py

# Rebuild the index
python scripts/build_browser.py

# Open the browser
open scripts/index.html
```

## GitHub Pages

The live site is deployed automatically:

**[https://jarvisxyz.github.io/buildingscience-archive/](https://jarvisxyz.github.io/buildingscience-archive/)**

> **Note:** The `archive/` directory (raw crawled HTML & assets) is excluded from the repository via `.gitignore` to keep the repo size manageable. The searchable UI works entirely from the generated `index.json`.

## License

This project is for personal archival and educational purposes. Content belongs to Building Science Corporation.
