#!/usr/bin/env python3
"""
buildingscience.com Full Archive Scraper
---------------------------------------
Scraps all content from buildingscience.com with:
- Complete HTML files preserved per page
- Extracted clean Markdown for each page
- All linked images/assets downloaded
- index.json with metadata for searchable browser UI

Structure:
  archive/
    documents/    - ~613 pages from /document-search/index
    other-event/  - ~99 past events
    video/        - ~13 videos
    service/      - ~4 service pages
    event/        - ~3 upcoming events
    bookstore/    - ~14 bookstore pages
    project/      - ~10 project pages
    users/        - ~6 author/contributor profiles
    bsl/          - ~4 building-science-live pages
    nodes/        - ~14 node pages
    sites/        - CSS/images from /sites/default/files/

Usage:
  pip install beautifulsoup4 lxml requests bleach html2text tqdm Pillow
  python3 scripts/scrape_buildingscience.py

Rate limit: 1 req/sec mandatory
"""

import os
import sys
import re
import time
import json
import hashlib
import urllib.parse
import html as html_module
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
import bleach
from html2text import HTML2Text
from tqdm import tqdm

BASE = "https://buildingscience.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# Rate limiting
RATE_LIMIT = 1.0  # seconds between requests
LAST_REQUEST_TIME = 0

# Base directory for the archive
ARCHIVE_DIR = Path(__file__).parent.parent / "archive"
META_FILE = Path(__file__).parent.parent / "index.json"

# Categories for the index
CATEGORY_MAP = {
    "documents": {"label": "Documents", "icon": "\ud83d\udcc4"},
    "contributors": {"label": "Contributors", "icon": "\ud83d\udc64"},
    "events": {"label": "Events", "icon": "\ud83d\udcc5"},
    "guides": {"label": "Guides", "icon": "\ud83d\udcd6"},
    "research": {"label": "Research", "icon": "\ud83d\udd2c"},
    "videos": {"label": "Videos", "icon": "\ud83d\udcfa"},
    "bookstore": {"label": "Bookstore", "icon": "\ud83d\udcda"},
    "services": {"label": "Services", "icon": "\ud83d\udd27"},
    "projects": {"label": "Projects", "icon": "\ud83d\udcca"},
}

TAGS = ["HVAC", "insulation", "moisture", "ventilation", "envelope",
        "energy-code", "residential", "commercial", "retrofit", "monitoring",
        "air-barriers", "thermal-bridging", "rainscreen", "crawlspaces",
        "foundations", "roofs-and-attics", "windows", "stucco",
        "passive-house", "net-zero", "building-science", "HVAC",
        "air-leakage", "vapor-control", "insulation-methods",
        "wall-assembly", "roof-assembly", "foundation-assembly",
        "indoor-air-quality", "humidity-control", "mold-prevention"]


def rate_limit():
    """Wait to maintain rate limit."""
    global LAST_REQUEST_TIME
    elapsed = time.time() - LAST_REQUEST_TIME
    if elapsed < RATE_LIMIT:
        time.sleep(RATE_LIMIT - elapsed)
    LAST_REQUEST_TIME = time.time()


def normalize_url(url):
    """Ensure a URL is absolute with the base domain."""
    if url.startswith("/"):
        return BASE + url
    if not url.startswith("http"):
        return BASE + "/" + url.lstrip("/")
    return url


def fetch(url):
    """Fetch a URL with rate limiting."""
    url = normalize_url(url)
    rate_limit()
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30, verify=True)
        resp.raise_for_status()
        return resp.text
    except requests.exceptions.RequestException as e:
        print(f"  [!] Error fetching {url}: {e}")
        return None


def sanitize_filename(name):
    """Create a safe directory name from a path."""
    # Remove leading slash
    name = name.lstrip("/")
    # Replace problematic chars
    name = re.sub(r'[<>:"\\|?*]', "_", name)
    name = re.sub(r"/", "-", name)
    # Remove consecutive underscores
    name = re.sub(r"_+", "_", name)
    name = name.strip("_")
    # Limit length
    if len(name) > 100:
        name = name[:100]
    return name or "unnamed"


def extract_title(html):
    """Extract the page title."""
    soup = BeautifulSoup(html, "lxml")
    # Try <title>
    title_tag = soup.find("title")
    if title_tag and title_tag.string:
        return title_tag.string.strip()
    # Try <h1>
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    return None


def extract_meta_descriptions(html, soup=None):
    """Extract title, meta description, and canonical URL."""
    if soup is None:
        soup = BeautifulSoup(html, "lxml")
    
    title = extract_title(html)
    
    # Meta description
    meta_desc = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag and desc_tag.get("content"):
        meta_desc = desc_tag["content"].strip()
    
    # Canonical URL
    canonical = ""
    link_tag = soup.find("link", rel="canonical")
    if link_tag and link_tag.get("href"):
        canonical = link_tag["href"].strip()
    
    # Tags from meta keywords
    keywords = []
    kw_tag = soup.find("meta", attrs={"name": "keywords"})
    if kw_tag and kw_tag.get("content"):
        keywords = [k.strip() for k in kw_tag["content"].split(",")]
    
    return title, meta_desc, canonical, keywords


def html_to_markdown(html, base_url):
    """Convert HTML body to clean Markdown."""
    soup = BeautifulSoup(html, "lxml")
    
    # Remove scripts, styles, nav, header, footer, sidebar, forms
    for tag in soup.find_all(["script", "style", "nav", "header", "footer", 
                               "aside", "form", "noscript"]):
        tag.decompose()
    
    # Remove elements with certain classes
    for cls in ["navigation", "sidebar", "footer", "header", "nav", "search",
                 "newsletter", "modal", "popup", "banner", "cookie", "ads",
                 "ad-banner", "skip-to-content"]:
        for elem in soup.find_all(class_=re.compile(cls, re.I)):
            elem.decompose()
    
    # Extract metadata from structured data
    tags = []
    for tag in soup.find_all("meta", attrs={"name": "keywords"}):
        if tag.get("content"):
            tags = [t.strip() for t in tag["content"].split(",")]
    
    # Also try article tags
    article = soup.find("article") or soup.find("main") or soup.find("div", class_="content")
    if article:
        body_html = str(article)
    else:
        body_html = str(soup.body) if soup.body else str(soup)
    
    # Convert to markdown
    h = HTML2Text()
    h.body_width = 0  # No line wrapping
    h.ignore_links = False
    h.ignore_images = True  # We handle images separately
    h.wrap_links = False
    h.wrap_tables = False
    h.mark_code = False
    h.emphasis_mark = "*"
    h.strong_mark = "**"
    h.single_line_break = True
    
    try:
        md = h.handle(body_html)
    except Exception:
        md = BeautifulSoup(body_html, "lxml").get_text(separator="\n", strip=True)
    
    # Clean up excessive blank lines
    md = re.sub(r"\n{4,}", "\n\n\n", md)
    md = md.strip()
    
    return md, tags


def download_assets(html, base_url, asset_dir):
    """Download all images and assets from the page."""
    soup = BeautifulSoup(html, "lxml")
    downloaded = []
    
    # Find all image sources
    img_tags = soup.find_all("img")
    for img in img_tags:
        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
        if not src:
            continue
        
        # Skip data URIs
        if src.startswith("data:"):
            continue
        
        full_url = urljoin(base_url, src)
        
        # Only download from buildingscience.com for local archive
        if "buildingscience.com" in full_url or full_url.startswith("//buildingscience.com") or full_url.startswith("/"):
            try:
                rate_limit()
                resp = requests.get(full_url, headers=HEADERS, timeout=15, verify=True)
                if resp.status_code == 200:
                    # Determine file extension
                    parsed = urlparse(full_url)
                    path = parsed.path
                    ext = os.path.splitext(path)[1] or ".jpg"
                    
                    # Sanitize filename
                    fname = sanitize_filename(os.path.basename(path))
                    ext = re.sub(r"[^a-z0-9]", "", ext.lower())
                    if not ext or ext == ".":
                        ext = ".jpg"
                    if ext:
                        fname = os.path.splitext(fname)[0][:50] + ext
                    
                    # Hash to avoid collisions
                    hash_suffix = hashlib.md5(full_url.encode()).hexdigest()[:8]
                    fname = f"{os.path.splitext(fname)[0]}_{hash_suffix}{ext}" if fname else f"asset_{hash_suffix}{ext}"
                    
                    fpath = asset_dir / fname
                    fpath.write_bytes(resp.content)
                    downloaded.append({
                        "original_url": full_url,
                        "local_path": str(fpath.relative_to(asset_dir.parent)),
                    })
            except Exception as e:
                pass  # Silently skip failed asset downloads
    
    return downloaded


def get_category_for_path(path):
    """Determine the archive category based on URL path."""
    if path.startswith("/documents/"):
        return "documents"
    elif path.startswith("/other-event/"):
        return "events"
    elif path.startswith("/video/"):
        return "videos"
    elif path.startswith("/service/"):
        return "services"
    elif path.startswith("/events/") and not path.startswith("/events/building-science"):
        return "events"
    elif path.startswith("/bookstore/"):
        return "bookstore"
    elif path.startswith("/project/"):
        return "projects"
    elif path.startswith("/users/"):
        return "contributors"
    elif "building-science-live" in path:
        return "videos"
    elif path.startswith("/node/"):
        return "documents"
    else:
        return "other"


def url_to_dir_path(url):
    """Convert a URL to a directory path within the archive."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    
    # Extract the document ID for /documents/ URLs
    if path.startswith("documents/"):
        parts = path.split("/")
        if len(parts) >= 3:
            # /documents/category/doc-id/view
            cat = parts[1]
            doc_id = parts[2]
            return f"documents/{sanitize_filename(cat)}/{sanitize_filename(doc_id)}"
        elif len(parts) >= 2:
            return f"documents/{sanitize_filename(parts[1])}"
    
    return sanitize_filename(path)


def extract_date(html):
    """Extract publication date from page."""
    soup = BeautifulSoup(html, "lxml")
    
    # Try structured data
    for schema in ["https://schema.org/DatePublished", "https://schema.org/datePublished"]:
        time_tag = soup.find("time", datetime=True)
        if time_tag:
            return time_tag["datetime"]
    
    # Try <meta name="date">
    date_tag = soup.find("meta", attrs={"name": "date"})
    if date_tag and date_tag.get("content"):
        return date_tag["content"]
    
    return None


def scrape_document(url, category="documents"):
    """Scrape a single document page."""
    url = normalize_url(url)
    print(f"  Fetching: {url}")

    # Determine directory path
    parsed = urlparse(url)
    dir_path = url_to_dir_path(url)
    html_path = ARCHIVE_DIR / dir_path

    # Skip if already scraped (resume support)
    if (html_path / "full.html").exists() and (html_path / "content.md").exists():
        # Reload metadata from existing files
        existing_html = (html_path / "full.html").read_text(encoding="utf-8")
        title, meta_desc, canonical, keywords = extract_meta_descriptions(existing_html)
        date = extract_date(existing_html)
        md = (html_path / "content.md").read_text(encoding="utf-8")
        asset_count = len(list((html_path / "assets").iterdir())) if (html_path / "assets").exists() else 0
        print(f"    (cached)")
        return {
            "url": url,
            "title": title or "Unknown",
            "description": meta_desc or "",
            "date": date or "",
            "tags": keywords[:20],
            "category": category,
            "local_path": str(html_path.relative_to(ARCHIVE_DIR)),
            "assets": asset_count,
            "word_count": len(md.split()) if md else 0,
        }

    html = fetch(url)
    if not html:
        return None
    
    title, meta_desc, canonical, keywords = extract_meta_descriptions(html)
    date = extract_date(html)
    category_label = "documents"
    
    # Save full HTML
    html_path.mkdir(parents=True, exist_ok=True)
    (html_path / "full.html").write_text(html, encoding="utf-8")
    
    # Extract markdown
    md, tags = html_to_markdown(html, url)
    (html_path / "content.md").write_text(md, encoding="utf-8")
    
    # Download assets
    asset_dir = html_path / "assets"
    downloaded = download_assets(html, url, asset_dir)
    
    # Determine category for index
    if category == "documents":
        index_category = "documents"
    elif category == "contributors":
        index_category = "contributors"
    elif category == "videos":
        index_category = "videos"
    elif category == "events":
        index_category = "events"
    elif category == "bookstore":
        index_category = "bookstore"
    elif category == "services":
        index_category = "services"
    elif category == "projects":
        index_category = "projects"
    else:
        index_category = "documents"
    
    return {
        "url": url,
        "title": title or "Unknown",
        "description": meta_desc or "",
        "date": date or "",
        "tags": list(set(keywords + tags))[:20],
        "category": index_category,
        "local_path": str(html_path.relative_to(ARCHIVE_DIR)),
        "assets": len(downloaded),
        "word_count": len(md.split()) if md else 0,
    }


def discover_document_urls():
    """Get all document URLs from sitemap.xml and the search index page."""
    all_urls = set()
    
    # Primary: Try sitemap.xml first (most comprehensive)
    print("Discovering URLs from sitemap.xml...")
    sitemap_url = f"{BASE}/sitemap.xml"
    html = fetch(sitemap_url)
    if html:
        soup = BeautifulSoup(html, "lxml")
        for loc in soup.find_all("loc"):
            url = loc.get_text(strip=True)
            if url and "buildingscience.com" in url:
                # Only include content pages, not taxonomy/feeds
                parsed = urlparse(url)
                path = parsed.path
                if any(path.startswith(p) for p in ["/documents/", "/other-event/", "/video/",
                    "/service/", "/events/", "/bookstore/", "/project/", "/users/",
                    "/building-science-live/", "/node/"]):
                    clean = path.rstrip("/")
                    all_urls.add(clean)
        print(f"  Found {len(all_urls)} URLs from sitemap.xml")
    
    # Secondary: Parse document search index with pagination
    print("Discovering document URLs from /document-search/index...")
    for page in range(0, 50):
        if page == 0:
            url = f"{BASE}/document-search/index"
        else:
            url = f"{BASE}/document-search/index?page={page}"
        
        html = fetch(url)
        if not html:
            break
        
        soup = BeautifulSoup(html, "lxml")
        new_urls = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/documents/"):
                clean = href.rstrip("/view").rstrip("/")
                if clean:
                    new_urls.add(clean)
        
        if not new_urls:
            break
        all_urls.update(new_urls)
        
        # Check for next page
        next_link = soup.find("a", string=re.compile(r"Next|›|»", re.I))
        if not next_link:
            break
    
    print(f"  Total: {len(all_urls)} document URLs")
    return sorted(all_urls)


def discover_past_event_urls():
    """Get all past event URLs from /past-events."""
    print("Discovering past event URLs from /past-events...")
    all_urls = set()
    page = 0
    
    while True:
        if page == 0:
            url = f"{BASE}/past-events"
        else:
            url = f"{BASE}/past-events?page={page}"
        
        html = fetch(url)
        if not html:
            break
        
        soup = BeautifulSoup(html, "lxml")
        new_urls = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/other-event/"):
                new_urls.add(href.rstrip("/"))
        
        if not new_urls:
            break
        all_urls.update(new_urls)
        
        # Check for next page
        if not soup.find("a", string=re.compile(r"Next|page", re.I)):
            break
        
        page += 1
        if page > 30:
            break
    
    print(f"  Found {len(all_urls)} past event URLs")
    return sorted(all_urls)


def discover_extra_urls():
    """Get URLs from other sections of the site."""
    extra = {}
    categories = {
        "/video/": ("video", "videos"),
        "/service/": ("service", "services"),
        "/events/": ("event", "events"),
        "/bookstore/": ("bookstore", "bookstore"),
        "/project/": ("project", "projects"),
        "/users/": ("user", "contributors"),
        "/building-science-live/": ("bsl", "videos"),
        "/node/": ("node", "documents"),
    }
    
    for path, (prefix, category) in categories.items():
        all_urls = set()
        full_prefix = f"/{prefix}"
        html = fetch(f"{BASE}{path}")
        if html:
            soup = BeautifulSoup(html, "lxml")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.startswith(full_prefix):
                    clean = href.rstrip("/").rstrip("/view")
                    all_urls.add(clean)
            # Also paginate
            for i in range(1, 10):
                html = fetch(f"{BASE}{path}?page={i}")
                if not html:
                    break
                soup = BeautifulSoup(html, "lxml")
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if href.startswith(full_prefix):
                        clean = href.rstrip("/").rstrip("/view")
                        all_urls.add(clean)
        
        print(f"  {category}: {len(all_urls)} URLs from {BASE}{path}")
        extra[category] = sorted(all_urls)
    
    # Get document-search index URLs as fallback for videos etc
    html = fetch(f"{BASE}/document-search/index")
    if html:
        soup = BeautifulSoup(html, "lxml")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            vid = href.startswith("/video/")
            if vid:
                # extra[category] is a list; convert to set, add, then back to list
                video_set = set(extra.get("videos", []))
                video_set.add(href.rstrip("/").rstrip("/view"))
                extra["videos"] = sorted(video_set)
    
    return extra


def build_index(metadata_list):
    """Build the index.json file."""
    # Collect all tags
    all_tags = set()
    for item in metadata_list:
        all_tags.update(item.get("tags", []))
    
    # Normalize tags
    normalized_tags = set()
    for t in all_tags:
        normalized_tags.add(t.lower().strip())
    for t in TAGS:
        normalized_tags.add(t)
    
    # Group by category
    items_by_cat = {}
    for item in metadata_list:
        cat = item["category"]
        if cat not in items_by_cat:
            items_by_cat[cat] = []
        items_by_cat[cat].append(item)
    
    categories = []
    for cat_id, cat_info in CATEGORY_MAP.items():
        if cat_id in items_by_cat:
            categories.append({
                "id": cat_id,
                "label": cat_info["label"],
                "icon": cat_info["icon"],
                "count": len(items_by_cat[cat_id]),
            })
    
    index = {
        "categories": categories,
        "total_documents": len(metadata_list),
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "https://buildingscience.com",
        "tags": sorted(list(normalized_tags)),
        "items": [],
    }
    
    for item in metadata_list:
        index["items"].append({
            "id": hashlib.md5(item["url"].encode()).hexdigest()[:8],
            "title": item["title"],
            "category": item["category"],
            "tags": item["tags"],
            "date": item["date"],
            "description": item["description"][:500],
            "url": item["url"],
            "local_path": item["local_path"],
            "word_count": item.get("word_count", 0),
            "assets": item.get("assets", 0),
        })
    
    return index


def main():
    print("=" * 60)
    print("buildingscience.com Archive Scraper")
    print("=" * 60)
    print(f"Archive directory: {ARCHIVE_DIR}")
    print(f"Rate limit: {RATE_LIMIT}s between requests")
    print()
    
    # Create archive directory
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Discover all URLs
    print("-" * 40)
    print("STEP 1: Discovering URLs")
    print("-" * 40)
    
    doc_urls = discover_document_urls()
    past_event_urls = discover_past_event_urls()
    extra_urls = discover_extra_urls()
    
    all_urls = {
        "documents": doc_urls,
        "events": past_event_urls,
        "videos": extra_urls.get("videos", []),
        "services": extra_urls.get("services", []),
        "bookstore": extra_urls.get("bookstore", []),
        "projects": extra_urls.get("projects", []),
        "contributors": extra_urls.get("contributors", []),
    }
    
    total_urls = sum(len(urls) for urls in all_urls.values())
    print(f"\nDiscovered {total_urls} URLs across {len(all_urls)} categories")
    
    # Summary
    for cat, urls in all_urls.items():
        print(f"  {cat}: {len(urls)} URLs")
    print()
    
    # Ask for confirmation (skip if --yes flag or non-interactive)
    print(f"Ready to scrape {total_urls} pages (estimated time: {total_urls * RATE_LIMIT / 60:.1f} minutes)")
    if "--yes" not in sys.argv and sys.stdin.isatty():
        response = input("\nProceed? (yes/y to continue): ").strip().lower()
        if response not in ("yes", "y"):
            print("Aborted.")
            sys.exit(0)
    else:
        print("\nRunning in non-interactive mode (--yes)")
    
    # Step 2: Scrape all URLs
    print("\n" + "=" * 60)
    print("STEP 2: Scraping all pages")
    print("=" * 60)
    
    metadata_list = []
    success_count = 0
    fail_count = 0
    
    for category, urls in all_urls.items():
        print(f"\nScraping [{category}]: {len(urls)} pages")
        print("-" * 40)
        
        for url in tqdm(urls, desc=category, leave=False):
            try:
                meta = scrape_document(url, category)
                if meta:
                    metadata_list.append(meta)
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                fail_count += 1
                print(f"  [!] Error: {e}")
        
        # Ensure rate limit before next category
        rate_limit()
    
    print(f"\n{'=' * 60}")
    print(f"COMPLETED: {success_count} succeeded, {fail_count} failed")
    print(f"{'=' * 60}")
    
    # Step 3: Generate index
    print("\nGenerating index.json...")
    index = build_index(metadata_list)
    META_FILE.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Written {META_FILE} ({len(metadata_list)} entries)")
    
    # Summary stats
    by_category = {}
    for item in metadata_list:
        cat = item["category"]
        if cat not in by_category:
            by_category[cat] = 0
        by_category[cat] += 1
    
    print(f"\nArchive Summary:")
    print(f"  Total pages: {len(metadata_list)}")
    for cat, count in sorted(by_category.items()):
        print(f"  {cat}: {count}")
    total_size = sum(
        (ARCHIVE_DIR / m["local_path"]).stat().st_size 
        for m in metadata_list 
        if (ARCHIVE_DIR / m["local_path"]).is_dir()
    )
    print(f"  Total archive size: {total_size / 1024 / 1024:.1f} MB")
    
    print(f"\nArchive complete at: {ARCHIVE_DIR}")
    print(f"Index at: {META_FILE}")


if __name__ == "__main__":
    main()
