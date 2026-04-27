#!/usr/bin/env python3
"""Generate the searchable browser UI for the buildingscience.com archive.

Outputs:
  scripts/index.json   — metadata for all archived documents
  scripts/index.html   — self-contained searchable interface
  scripts/index.html   — self-contained searchable interface (reads index.json)

Uses Fuse.js (CDN) for client-side search. Dark/light theme, category filters, tag filters, sort by title/date.
"""

import os, sys, re
from pathlib import Path
from bs4 import BeautifulSoup

INDEX_FILE = Path(__file__).parent.parent / "archive" / "documents" / "INDEX"
OUTPUT_DIR = Path(__file__).parent.parent
INDEX_JSON = OUTPUT_DIR / "index.json"
INDEX_HTML = OUTPUT_DIR / "index.html"

def build_index_from_archive(data):
    """Build index.json from scraped data."""
    from pathlib import Path
    from urllib.parse import unquote
    import hashlib

    results = []
    archive_root = OUTPUT_DIR.parent / "archive"

    # Walk through all category directories
    for cat_dir in archive_root.iterdir():
        if not cat_dir.is_dir():
            continue
        cat_name = cat_dir.name
        
        for sub_dir in cat_dir.iterdir():
            if not sub_dir.is_dir():
                continue
            
            for doc_dir in sub_dir.iterdir():
                if not doc_dir.is_dir():
                    continue
                
                # Find full.html file
                full_html = doc_dir / "full.html"
                content_md = doc_dir / "content.md"
                assets_dir = doc_dir / "assets"
                
                if not full_html.exists():
                    continue
                
                html_content = full_html.read_text(encoding="utf-8", errors="replace")
                soup = BeautifulSoup(html_content, "html.parser")
                
                # Extract title
                title_tag = soup.find("title")
                title = title_tag.get_text(strip=True) if title_tag else "Untitled"
                
                # Extract description
                desc_meta = soup.find("meta", attrs={"name": "description"})
                description = desc_meta.get("content", "") if desc_meta else ""
                if not description:
                    og_desc = soup.find("meta", attrs={"property": "og:description"})
                    description = og_desc.get("content", "") if og_desc else ""
                
                # Extract tags
                tags = []
                tag_elements = soup.select(".field--name-field-tags a, .taxonomy-container a")
                for a in tag_elements:
                    t = a.get_text(strip=True)
                    if t and t not in tags:
                        tags.append(t)
                
                # Extract date
                date_meta = soup.find("meta", attrs={"name": "date"})
                date = date_meta.get("content", "") if date_meta else ""
                if not date:
                    pubdate = soup.find("meta", attrs={"property": "article:published_time"})
                    date = pubdate.get("content", "") if pubdate else ""
                
                # Determine URL
                # The URL is the parent directory's name
                url = str(doc_dir.parent / doc_dir.name)
                full_url = unquote(f"{BASE_URL}{url}")
                
                # Count assets
                asset_count = len([f for f in assets_dir.iterdir() if f.is_file()]) if assets_dir.exists() else 0
                
                results.append({
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "date": date,
                    "type": cat_name,
                    "doc_subtype": sub_dir.name,
                    "url": full_url,
                    "directory": str(doc_dir.relative_to(archive_root)),
                    "html_file": str(full_html),
                    "md_file": str(content_md) if content_md.exists() else "",
                    "asset_count": asset_count,
                })

    return results

def build_html(index_data):
    """Build the complete searchable browser UI."""
    
    # Escape for JSON embedding
    json_str = json.dumps(index_data, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Buildingscience.com Archive</title>
<script src="https://cdn.jsdelivr.net/npm/fuse.js@7.0.0/dist/fuse.min.js"></script>
<style>
:host {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}}

:root {{
    --bg: #0f172a;
    --bg-card: #1e293b;
    --text: #e2e8f0;
    --text-muted: #94a3b8;
    --border: #334155;
    --accent: #3b82f6;
    --accent-hover: #60a5fa;
    --tag-bg: #1e3a5f;
    --tag-text: #93c5fd;
    --sidebar-bg: #1e293b;
    --highlight: #854d0e;
    --shadow: 0 1px 3px rgba(0,0,0,0.4);
}}

[data-theme="light"] {{
    --bg: #f5f5f5;
    --bg-card: #ffffff;
    --text: #1a1a1a;
    --text-muted: #666;
    --border: #ddd;
    --accent: #2563eb;
    --accent-hover: #1d4ed8;
    --tag-bg: #e0e7ff;
    --tag-text: #3730a3;
    --sidebar-bg: #f9fafb;
    --highlight: #fef3c7;
    --shadow: 0 1px 3px rgba(0,0,0,0.1);
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
}}

.app {{
    display: flex;
    min-height: 100vh;
}}

/* Sidebar */
.sidebar {{
    width: 280px;
    background: var(--sidebar-bg);
    border-right: 1px solid var(--border);
    padding: 24px 0;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    overflow-y: auto;
    z-index: 100;
    transition: transform 0.3s ease;
}}

.sidebar.collapsed {{
    transform: translateX(-100%);
}}

.sidebar-header {{
    padding: 0 20px 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 16px;
}}

.sidebar-header h1 {{
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 4px;
}}

.sidebar-header p {{
    font-size: 12px;
    color: var(--text-muted);
}}

.sidebar-nav {{
    list-style: none;
    padding: 0;
}}

.sidebar-nav li {{
    padding: 8px 20px;
    cursor: pointer;
    font-size: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: background 0.15s;
}}

.sidebar-nav li:hover {{
    background: var(--accent);
    color: white;
}}

.sidebar-nav li.active,
.sidebar-nav li.active:hover {{
    background: var(--accent);
    color: white;
    font-weight: 600;
}}

.sidebar-nav .count {{
    font-size: 11px;
    opacity: 0.6;
    background: var(--border);
    padding: 2px 6px;
    border-radius: 10px;
    min-width: 24px;
    text-align: center;
}}

/* Main content */
.main {{
    flex: 1;
    margin-left: 280px;
    min-height: 100vh;
}}

/* Top bar */
.topbar {{
    background: bg-card;
    border-bottom: 1px solid var(--border);
    padding: 16px 24px;
    position: sticky;
    top: 0;
    z-index: 50;
    display: flex;
    gap: 12px;
    align-items: center;
    box-shadow: var(--shadow);
}}

.search-box {{
    flex: 1;
    position: relative;
}}

.search-box input {{
    width: 100%;
    padding: 10px 16px 10px 40px;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 15px;
    background: var(--bg);
    color: var(--text);
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
}}

.search-box input:focus {{
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}}

.search-box .search-icon {{
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
}}

.topbar-controls {{
    display: flex;
    gap: 8px;
    align-items: center;
}}

.btn {{
    padding: 8px 16px;
    border: 1px solid var(--border);
    border-radius: 6px;
    background: var(--bg);
    color: var(--text);
    cursor: pointer;
    font-size: 13px;
    transition: all 0.15s;
    display: flex;
    align-items: center;
    gap: 4px;
}}

.btn:hover {{
    background: var(--accent);
    color: white;
    border-color: var(--accent);
}}

.btn.active {{
    background: var(--accent);
    color: white;
    border-color: var(--accent);
}}

.stats {{
    font-size: 12px;
    color: var(--text-muted);
    padding: 0 24px 8px;
}}

/* Results */
.results-container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px 48px;
}}

.category-header {{
    font-size: 20px;
    font-weight: 700;
    margin: 32px 0 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--accent);
    color: var(--accent);
}}

.results-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 16px;
    margin-top: 16px;
}}

.card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    transition: box-shadow 0.2s, transform 0.15s;
    box-shadow: var(--shadow);
    cursor: pointer;
    text-decoration: none;
    color: inherit;
    display: block;
}}

.card:hover {{
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transform: translateY(-2px);
}}

.card-link {{
    color: var(--accent);
    font-size: 12px;
    text-decoration: none;
    word-break: break-all;
}}

.card-link:hover {{
    text-decoration: underline;
}}

.card-title {{
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 8px;
    line-height: 1.4;
}}

.card-meta {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 8px;
}}

.card-meta .tag {{
    font-size: 11px;
    padding: 2px 8px;
    background: var(--tag-bg);
    color: var(--tag-text);
    border-radius: 4px;
}}

.card-desc {{
    font-size: 13px;
    color: var(--text-muted);
    line-height: 1.5;
}}

.card-desc em {{
    background: var(--highlight);
    padding: 0 2px;
    font-style: normal;
    font-weight: 600;
}}

.card-type {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-muted);
    margin-bottom: 4px;
}}

.card-date {{
    font-size: 11px;
    color: var(--text-muted);
    margin-bottom: 8px;
}}

/* Empty state */
.empty-state {{
    text-align: center;
    padding: 64px 24px;
    color: var(--text-muted);
}}

.empty-state h2 {{
    font-size: 24px;
    margin-bottom: 8px;
    color: var(--text);
}}

/* Mobile */
@media (max-width: 768px) {{
    .sidebar {{
        position: fixed;
        transform: translateX(-100%);
    }}
    .sidebar.open {{
        transform: translateX(0);
    }}
    .main {{
        margin-left: 0;
    }}
    .mobile-toggle {{
        display: block !important;
    }}
    .results-grid {{
        grid-template-columns: 1fr;
    }}
}}

.mobile-toggle {{
    display: none;
}}

.mobile-overlay {{
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.5);
    z-index: 90;
}}

.mobile-overlay.active {{
    display: block;
}}

/* Pagination */
.pagination {{
    display: flex;
    justify-content: center;
    gap: 4px;
    margin-top: 32px;
}}

.page-btn {{
    padding: 6px 12px;
    border: 1px solid var(--border);
    border-radius: 4px;
    background: var(--bg);
    cursor: pointer;
    font-size: 13px;
    color: var(--text);
}}

.page-btn:hover, .page-btn.active {{
    background: var(--accent);
    color: white;
    border-color: var(--accent);
}}

/* Sort bar */
.sort-bar {{
    display: flex;
    gap: 4px;
    margin-top: 8px;
}}

/* Footer */
.footer {{
    text-align: center;
    padding: 32px 24px;
    border-top: 1px solid var(--border);
    color: var(--text-muted);
    font-size: 12px;
}}

/* Toggle sidebar button */
.sidebar-toggle {{
    background: none;
    border: none;
    cursor: pointer;
    font-size: 18px;
    color: var(--text-muted);
    padding: 8px;
    border-radius: 4px;
}}

.sidebar-toggle:hover {{
    color: var(--text);
}}

/* Loading */
.loading {{
    text-align: center;
    padding: 48px;
    color: var(--text-muted);
}}

.loading .spinner {{
    display: inline-block;
    width: 40px;
    height: 40px;
    border: 3px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-bottom: 16px;
}}

@keyframes spin {{
    to {{ transform: rotate(360deg); }}
}}
</style>
</head>
<body>
<div class="app">
    <!-- Mobile overlay -->
    <div class="mobile-overlay" id="mobileOverlay"></div>

    <!-- Sidebar -->
    <aside class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <h1>📚 Building Science Archive</h1>
            <p id="totalCount">Loading...</p>
        </div>
        <ul class="sidebar-nav" id="sidebarNav">
            <li class="active" data-cat="all">All <span class="count" id="countAll">0</span></li>
        </ul>
    </aside>

    <!-- Main -->
    <main class="main">
        <!-- Top bar -->
        <div class="topbar">
            <button class="btn mobile-toggle" id="mobileToggle">&#9776;</button>
            <button class="sidebar-toggle" id="sidebarToggle">&#9776;</button>
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="text" id="searchInput" placeholder="Search documents, topics, tags..." autocomplete="off">
            </div>
            <div class="topbar-controls">
                <button class="btn" id="themeToggle" title="Toggle theme">🌙</button>
                <button class="btn" id="sortToggle" title="Toggle sort">↕ Sort</button>
                <button class="btn" id="exportBtn" title="Export index">💾 Save</button>
            </div>
        </div>

        <div class="stats" id="resultStats"></div>

        <div class="sort-bar" id="sortBar" style="display:none; max-width:1200px; margin:8px auto; padding:0 24px;">
            <button class="btn" data-sort="title">Title</button>
            <button class="btn" data-sort="date">Date</button>
            <button class="btn" data-sort="type">Type</button>
        </div>

        <!-- Results -->
        <div class="results-container" id="resultsContainer">
            <div class="loading">
                <div class="spinner"></div>
                <p>Loading index...</p>
            </div>
        </div>

        <div class="footer">
            <p>Archive of <a href="https://buildingscience.com" style="color:var(--accent)">buildingscience.com</a> — for personal use only</p>
            <p style="margin-top:4px" id="lastUpdated">Data last updated: Unknown</p>
        </div>
    </main>
</div>

<script>
// Embedded data from index.json
const DOCUMENTS = {json_str};
const PER_PAGE = 24;

// State
let fuse = null;
let filteredDocs = [...DOCUMENTS];
let currentCategory = 'all';
let currentSort = 'relevance';
let currentPage = 1;
let currentSearch = '';

// Init
function init({{ docs }}) {{
    // Build search index
    const options = {{
        keys: [
            {{ name: 'title', weight: 0.4 }},
            {{ name: 'description', weight: 0.3 }},
            {{ name: 'tags', weight: 0.2 }},
            {{ name: 'doc_subtype', weight: 0.1 }}
        ],
        includeScore: true,
        threshold: 0.3,
        ignoreLocation: true,
        minMatchCharLength: 2
    }};
    fuse = new Fuse(docs, options);

    // Build category sidebar
    buildCategoryNav();

    // Show all
    filteredDocs = [...docs];
    render();

    // Last updated
    const lastUpdated = document.getElementById('lastUpdated');
    const match = LOCATION_FILE.match(/\d{{4}}-\d{{2}}-\d{{2}}/);
    if (match) lastUpdated.textContent = 'Data last updated: ' + match[0];
    else lastUpdated.textContent = 'Loaded locally';

    // Event listeners
    document.getElementById('sidebarToggle').addEventListener('click', toggleSidebar);
    document.getElementById('mobileToggle').addEventListener('click', toggleMobileSidebar);
    document.getElementById('mobileOverlay').addEventListener('click', toggleMobileSidebar);
    document.getElementById('themeToggle').addEventListener('click', toggleTheme);
    document.getElementById('sortToggle').addEventListener('click', toggleSortBar);
    document.getElementById('exportBtn').addEventListener('click', exportIndex);

    // Search
    let searchTimeout;
    document.getElementById('searchInput').addEventListener('input', (e) => {{
        clearTimeout(searchTimeout);
        currentSearch = e.target.value.trim();
        if (currentSearch.length < 2) {{
            filterByCategory(currentCategory);
            return;
        }}
        searchTimeout = setTimeout(() => {{
            performSearch(currentSearch);
        }}, 200);
    }});

    // Restore theme
    const saved = localStorage.getItem('bs-theme');
    if (saved === 'light') toggleTheme();
}}

function buildCategoryNav({{ docs }}) {{{{
    const cats = new Set();
    docs.forEach(d => {{
        const cat = d.type || 'other';
        const sub = d.doc_subtype || '';
        cats.add(cat + (sub ? ':' + sub : ''));
    }});

    const counts = {{$}};
    docs.forEach(d => {{
        const cat = d.type || 'other';
        const sub = d.doc_subtype || '';
        const key = sub ? cat + ':' + sub : cat;
        counts[key] = (counts[key] || 0) + 1;
        counts[cat] = (counts[cat] || 0) + 1;
    }});

    const nav = document.getElementById('sidebarNav');
    const allCount = document.getElementById('countAll');
    allCount.textContent = docs.length;
    document.getElementById('totalCount').textContent =
        `${{docs.length}} documents,{{Object.keys(cats).length }} categories`;

    // Category names
    const catNames = {{$}};

    const order = [
        'all', 'document', 'report', 'digest', 'insight', 'published-article',
        'conference-paper', 'case-study', 'guide', 'houseplan', 'enclosure',
        'bareport', 'special', 'contributor', 'event', 'project', 'service',
        'glossary', 'conversation', 'video', 'bookstore'
    ];

    const displayed = new Set(['all']);

    for (const cat of order) {{{{
        if (!cats.has(cat) && !cats.has(cat + ':')) continue;
        if (displayed.has(cat)) continue;
        displayed.add(cat);
        const li = document.createElement('li');
        const subCats = Array.from(cats.keys()).filter(c => c.startsWith(cat + ':') || c === cat);
        const total = subCats.reduce((sum, c) => sum + counts[c], 0) + counts[cat];
        li.innerHTML = `<span>${{$}}catNames[cat] || cat.replace('-', ' ').toUpperCase()}}</span> <span class="count">${{$}}total || counts[cat] || 0}}</span>`;
        li.dataset.cat = cat;
        li.addEventListener('click', () => filterByCategory(cat));
        nav.appendChild(li);
    }}}}

    // Subcategories
    const subByParent = new Map();
    for (const key of cats.keys()) {{{{
        const [parent] = key.split(':');
        if (!subByParent.has(parent)) subByParent.set(parent, []);
        subByParent.get(parent).push(key);
    }}}}

    for (const parent of subByParent.keys()) {{{{
        if (order.includes(parent)) continue;
        // Add subcategories as separate items or nested
    }}}}
}}}}

function filterByCategory(cat) {{{{
    currentCategory = cat;
    currentPage = 1;
    document.getElementById('searchInput').value = document.getElementById('searchInput').value = '';
    currentSearch = '';

    document.querySelectorAll('.sidebar-nav li').forEach(li => {{{{
        li.classList.toggle('active', li.dataset.cat === cat);
    }}));

    if (cat === 'all') {{{{
        filteredDocs = [...filteredDocs];
    }} else {{{{
        filteredDocs = docs.filter(d =>
            d.type === cat || d.doc_subtype === cat || d.doc_subtype === cat.replace('-', '')
        );
    }}

    if (currentSearch.length >= 2) {{{{
        performSearch(currentSearch);
    }}

    render();
}}}}

function performSearch(query) {{{{
    if (!fuse || query.length < 2) {{{{
        if (currentCategory === 'all') {{{{
            filteredDocs = [...filteredDocs];
        }} else {{{{
            filteredDocs = docs.filter(d => d.type === currentCategory);
        }}
        return;
    }}

    const results = fuse.search(query);
    filteredDocs = results.map(r => r.item);
}}}}

function render() {{{{
    const container = document.getElementById('resultsContainer');
    const stats = document.getElementById('resultStats');

    if (filteredDocs.length === 0) {{{{
        if (currentSearch) {{{{
            container.innerHTML = `
                <div class="empty-state">
                    <h2>No results found</h2>
                    <p>Try different keywords or clear your search.</p>
                </div>
            `;
        }} else {{{{
            container.innerHTML = '<div class="empty-state"><h2>No documents</h2></div>';
        }}
        stats.textContent = '0 results';
        return;
    }}

    // Sort
    const sorted = sortResults(filteredDocs);

    // Pagination
    const totalPages = Math.ceil(sorted.length / PER_PAGE);
    const start = (currentPage - 1) * PER_PAGE;
    const pageDocs = sorted.slice(start, start + PER_PAGE);

    stats.textContent = document.getElementById('resultStats').textContent = `Showing ${{$}}start + 1}}-{{Math.min(start + PER_PAGE, sorted.length)}} of ${{$}}sorted.length}} results`;

    // Group by category
    const groups = groupByCategory(pageDocs);

    let html = '';
    for (const [cat, docs] of Object.entries(groups)) {{{{
        const catNames = {{$}};

        html += `<div class="category-header" style="text-transform:capitalize;">${{$}}catNames[cat] || cat.replace('-', ' ').toUpperCase()}}</div>`;
        html += '<div class="results-grid">';
        docs.forEach(doc => {{{{ html += renderCard(doc); }}});
        html += '</div>';
    }}}

    if (totalPages > 1) {{{{
        html += '<div class="pagination">';
        for (let p = 1; p <= totalPages; p++) {{{{
            let classStr = p === currentPage ? 'active' : '';
            html += `<button class="page-btn ${{$}}classStr}}">${{$}}p}}</button>`;
        }}}
        html += '</div>';
    }}}

    container.innerHTML = html;

    // Wire up pagination
    container.querySelectorAll('.page-btn').forEach(btn => {{{{
        btn.addEventListener('click', () => {{{{
            const page = parseInt(btn.textContent);
            if (page >= 1 && page <= totalPages) {{{{
                currentPage = page;
                render();
                window.scrollTo(0, window.scrollTo(0;
            }}}
        }});
    }}}
}}

function renderCard(doc) {{{{
    const title = doc.title || 'Untitled';
    const desc = doc.description || '';
    const tags = doc.tags || [];
    const date = doc.date || '';
    const type = doc.type || '';
    const url = doc.url || '';
    const directory = doc.directory || '';

    let tagHtml = '';
    if (tags.length > 0) {{{{
        tagHtml = '<div class="card-meta">tags.slice(0, 5).map(t => `<span class="tag">${{$}}escapeHtml(t)}</span>`).join('') + '</div>';
    }}}

    let descHtml = '';
    if (desc) {{{{
        const cleanDesc = desc.replace(/<[^>]*>/g, '').substring(0, 500);
        descHtml = `<div class="card-desc">${{$}}escapeHtml(cleanDesc)}}</div>`;
    }}}

    let dateHtml = '';
    if (date) dateHtml = `<div class="card-date">${{$}}new Date(date).toLocaleDateString('en-US', {{ year: 'numeric', month: 'short', day: 'numeric' }})}}</div>`;

    const fullPath = 'https://example.com/' + directory + '/full.html';

    return `
        <a class="card" href="${{$}}fullPath}}" target="_blank" rel="noopener"">">
            <div class="card-type">${{$}}(type || '').toUpperCase() }}</div>
            <div class="card-title">${{$}}escapeHtml(title)}}</div>
            ${{$}}dateHtml if date else ''}}
            ${{$}}tagHtml}}
            ${{$}}descHtml}}
            <div class="card-meta" style="margin-top:8px;">
                <span class="tag">📄 HTML</span>
                <span class="tag">📝 Markdown</span>
            </div>
        </a>
    `;
}}

function escapeHtml(str) {{{{
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}}

function sortResults(docs) {{{{
    const sorted = [...docs];
    if (currentSort === 'title') {{{{
        sorted.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
    }} else if (currentSort === 'date') {{{{
        sorted.sort((a, b) => {{{{
            const da = a.date ? new Date(a.date) : new Date(0);
            const db = b.date ? new Date(b.date) : new Date(0);
            return db - da;
        }}});
    }} else if (currentSort === 'relevance') {{{{
        // Keep original order
    }}}
    return sorted;
}}

function groupByCategory(docs) {{{{
    const groups = {{$}};
    docs.forEach(doc => {{{{
        const cat = doc.doc_subtitle || doc.type || 'unknown';
        if (!groups[cat]) groups[cat] = [];
        groups[cat].push(doc);
    }}};
    return groups;
}}

// Theme
function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('bs-theme', next);
    document.getElementById('themeToggle').textContent = next === 'dark' ? '🌙' : '☀';
}}

function toggleSidebar() {{{{
    document.getElementById('sidebar').classList.toggle('collapsed');
}}

function toggleMobileSidebar() {{{{
    document.getElementById('sidebar').classList.toggle('open');
    document.getElementById('mobileOverlay').classList.toggle('active');
}}

function toggleSortBar() {{{{
    const bar = document.getElementById('sortBar');
    if (bar.style.display === 'none') {{{{
        bar.style.display = 'flex';
    }} else {{{{
        bar.style.display = 'none';
        document.getElementById('sortToggle').textContent = '↕ Sort';
    }}}
}}

document.addEventListener('click', (e) => {{{{
    if (e.target.closest('[data-sort]')) {{{{
        const sort = e.target.dataset.sort;
        document.querySelectorAll('[data-sort]').forEach(btn => btn.classList.remove('active'));
        e.target.classList.add('active');
        document.getElementById('sortToggle').textContent =
            sort === 'title' ? 'A-Z' : sort === 'date' ? 'Date' : '${{$}}↕ Sort';
        currentSort = sort;
        render();
    }}}
}});

function exportIndex() {{{{
    const blob = new Blob([JSON.stringify(DOCUMENTS, null, 2)], {{ type: 'application/json' }});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'index.json';
    a.click();
    URL.revokeObjectURL(url);
}}

// Load index if no embedded data
if (typeof DOCUMENTS === 'undefined' || !DOCUMENTS || DOCUMENTS.length === 0) {{{{
    document.querySelector('.spinner').outerHTML = '';
    fetch('index.json').then(r => r.json()).then(data => {{{{
        window.DOCUMENTS = data;
        init(data);
    }}}).catch(() => {{{{
        document.getElementById('resultsContainer').innerHTML =
            '<div class="empty-state"><h2>No data</h2><p>No index.json found.</p></div></div>';;
    }});} else {
    init(DOCUMENTS);
}}
</script>
</body>
</html>

"""

# Write files
OUTPUT_FILE = Path(__file__).parent.parent / "index.json"
OUTPUT_FILE.write_text(json.dumps(INDEX_DATA, indent=2, ensure_ascii=False), encoding="utf-8")
INDEX_HTML.write_text(HTML_TEMPLATE, encoding="utf-8")
print(f"Written {OUTPUT_FILE} and {INDEX_HTML}")

