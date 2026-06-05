# Architecture

## 1. High-Level Overview

`image-sitemap` is an async Python library that crawls websites, discovers pages and images, and generates XML sitemap files conforming to the sitemap protocol for search engine submission. It is published on PyPI as `image-sitemap` (`Observed`: `pyproject.toml` `[project] name`).

The library solves two problems: (1) recursive URL discovery across a website's link graph, and (2) extraction and indexing of image URLs per page, producing both standard and image sitemap XML files (`Inferred` from `pyproject.toml` description and the two distinct sitemap templates in `src/image_sitemap/instruments/templates.py`).

The architecture is a single-process, async pipeline: a public `Sitemap` facade orchestrates two single-responsibility crawlers (`LinksCrawler`, `ImagesCrawler`) backed by shared instrument utilities for HTTP, configuration, and file output. All I/O is async via `aiohttp` and `asyncio`; there is no server component (`Observed`: all source under `src/image_sitemap/`, dependency on `aiohttp` in `pyproject.toml`).

Evidence anchors: `pyproject.toml`, `src/image_sitemap/main.py`, `src/image_sitemap/links_crawler.py`, `src/image_sitemap/images_crawler.py`, `src/image_sitemap/instruments/web.py`, `src/image_sitemap/instruments/templates.py`.

## 2. System Architecture (Logical)

Four logical components, all within a single package:

1. **Public API** (`Sitemap` class in `main.py`) — Facade that consumers instantiate. Exposes five async methods for crawling links, generating sitemaps, and extracting image data. Owns no crawl state between calls.

2. **Link Discovery** (`LinksCrawler` in `links_crawler.py`) — Recursive BFS crawler that discovers URLs within a domain, respecting depth limits, subdomain rules, and file-extension exclusions. Returns a set of crawled URLs.

3. **Image Extraction** (`ImagesCrawler` in `images_crawler.py`) — Extracts image URLs from HTML pages, filters by MIME type, excludes data URIs. Returns a dict mapping page URLs to image URL lists.

4. **Instruments** (`instruments/`) — Shared utility layer:
   - `Config` — Frozen dataclass of ~30 fields controlling all crawl behavior.
   - `WebInstrument` — Sole HTTP client (`aiohttp`) plus HTML parsing (`BeautifulSoup`) and URL filtering.
   - `FileInstrument` — Builds and writes XML sitemap files.
   - `templates.py` — XML template strings for sitemap and image-sitemap formats.

Dependency direction:

```
Sitemap (main.py)
  ├──→ LinksCrawler ──→ Instruments (WebInstrument, Config)
  ├──→ ImagesCrawler ──→ Instruments (WebInstrument, Config)
  └──→ Instruments (FileInstrument, Config)
```

Key boundaries:
- Crawlers never import each other (`Observed`: no cross-imports between `links_crawler.py` and `images_crawler.py`).
- `FileInstrument` has no dependency on `WebInstrument` or `Config` — it receives only plain data (`Observed`: imports only `templates` and `typing`).
- `Config` has no dependencies on any other package module — pure data (`Observed`: imports only `dataclasses`, `typing`).
- There is intentionally no persistence layer, no database, and no external service integration beyond HTTP crawling of the target site.

## 3. Code Map (Physical)

```
image_sitemap/                          # Repository root
├── src/image_sitemap/                  # Library source (the only code root)
│   ├── __init__.py                     # Exports Sitemap, __version__
│   ├── __version__.py                  # Version string
│   ├── main.py                         # Sitemap class — public API entry point
│   ├── links_crawler.py                # LinksCrawler — recursive URL discovery
│   ├── images_crawler.py               # ImagesCrawler — image extraction + filtering
│   └── instruments/                    # Shared utility layer (see below)
│       ├── __init__.py                 # Re-exports WebInstrument
│       ├── config.py                   # Config dataclass (~30 fields)
│       ├── web.py                      # WebInstrument — HTTP, parsing, URL filtering
│       ├── file.py                     # FileInstrument — XML file generation
│       └── templates.py                # XML template strings
├── example.py                          # End-to-end smoke test (crawls rucaptcha.com)
├── pyproject.toml                      # Build config, dependencies, tool settings
├── Makefile                            # lint, refactor, build, upload, test targets
├── AGENTS.md                           # Repository-level contributor rules
├── src/image_sitemap/instruments/AGENTS.md  # Instruments subsystem local rules
└── README.md                           # Usage docs and config field descriptions
```

Where is X?

- **Public API surface**: `src/image_sitemap/main.py` — the `Sitemap` class.
- **Crawl configuration**: `src/image_sitemap/instruments/config.py` — the `Config` dataclass.
- **HTTP requests / HTML parsing**: `src/image_sitemap/instruments/web.py` — `WebInstrument`.
- **XML output format**: `src/image_sitemap/instruments/templates.py` + `file.py`.
- **URL discovery logic**: `src/image_sitemap/links_crawler.py`.
- **Image extraction logic**: `src/image_sitemap/images_crawler.py`.
- **Runnable example**: `example.py` at repository root.

## 4. Life of a Request / Primary Data Flow

This is a library, not a service. The primary flow is a CLI/library call pipeline:

```
User code
  → Sitemap(config).run_images_sitemap(url)          # main.py — public entry
    → LinksCrawler.run()                              # links_crawler.py — BFS crawl
      → WebInstrument.download_page(url)              # web.py — HTTP GET, retry (6 attempts)
      → WebInstrument.filter_links(...)               # web.py — domain, subdomain, extension filters
      → Recursive __links_crawler for each link       # links_crawler.py — depth-limited BFS
    → ImagesCrawler.get_data(links)                   # images_crawler.py — extract images per page
      → WebInstrument.download_page(url)              # web.py — fetch each page
      → WebInstrument.find_tags(html, "img", "src")   # web.py — BeautifulSoup tag extraction
      → __filter_images_links(image_urls)             # images_crawler.py — MIME type + data URI filter
    → FileInstrument.create_image_sitemap(data)       # file.py — build XML from templates, write file
```

For a standard (non-image) sitemap, the flow is similar but omits `ImagesCrawler`, using `LinksCrawler.create_sitemap()` instead (`Observed`: `Sitemap.run_sitemap()` and `LinksCrawler.create_sitemap()`).

## 5. Architectural Invariants & Constraints

- **Rule**: All HTTP requests must go through `WebInstrument.download_page()`. No raw `aiohttp` calls elsewhere.
  - **Rationale**: Centralizes retry logic (exponential backoff, 6 attempts), user-agent headers, and connection pooling.
  - **Enforcement / Signals** (`Inferred`): Convention only — no build-time or lint enforcement observed.

- **Rule**: All behavioral parameters flow through `Config` fields. No ad-hoc parameters on crawler or instrument methods beyond `Config` and URLs.
  - **Rationale**: Single source of truth for crawl behavior; callers configure once via `Config`.
  - **Enforcement / Signals** (`Observed`): All crawler constructors accept `(init_url, config)` or `(config)` only.

- **Rule**: `LinksCrawler` and `ImagesCrawler` never import each other.
  - **Rationale**: Single-responsibility separation — URL discovery is independent of image extraction.
  - **Enforcement / Signals** (`Observed`): No cross-imports in source files.

- **Rule**: HTML parsing must use `BeautifulSoup`, never regex.
  - **Rationale**: Robustness against malformed HTML.
  - **Enforcement / Signals** (`Inferred`): Convention stated in `AGENTS.md`; `web.py` uses `bs4` exclusively.

- **Rule**: No sync HTTP — all network I/O uses `asyncio`/`aiohttp`.
  - **Rationale**: Performance for concurrent page crawling.
  - **Enforcement / Signals** (`Observed`): `requests` is not a dependency; `web.py` uses `aiohttp` exclusively.

- **Rule**: `FileInstrument` uses synchronous file I/O and runs only after async crawling completes.
  - **Rationale**: File writes are fast and occur once, outside the event loop.
  - **Enforcement / Signals** (`Observed`): `file.py` uses standard `open()`, not `aiofiles`.

- **Rule**: `nofollow` links must be excluded during link filtering.
  - **Rationale**: Respects site owner crawl preferences; SEO compliance.
  - **Enforcement / Signals** (`Observed`): `web.py` filters `rel="nofollow"` links.

- **Rule**: Python 3.12+ only; modern type syntax (`dict[str, str]` not `Dict`).
  - **Rationale**: Modern stdlib generics; no `typing` legacy aliases.
  - **Enforcement / Signals** (`Observed`): `pyproject.toml` sets `requires-python = ">=3.12"`; source uses lowercase generics.

- **Rule**: No `print()` — use `logging.getLogger(__name__)`.
  - **Rationale**: Library consumers control log output.
  - **Enforcement / Signals** (`Inferred`): Convention stated in `AGENTS.md`; source uses `logging` module.

## 6. Documentation Strategy

`ARCHITECTURE.md` (this file) serves as the global map and invariant reference for the repository.

Module-level detail lives in:
- `AGENTS.md` — repository-wide contributor conventions and change rules.
- `src/image_sitemap/instruments/AGENTS.md` — local rules and boundaries for the instruments subsystem.
- `README.md` — usage examples, configuration field descriptions, and API documentation.

What belongs where:
- **Global architecture docs** (`ARCHITECTURE.md`): component layout, dependency direction, invariants, primary data flow.
- **Local module docs** (`AGENTS.md` in subdirectories): safe-change rules, gotchas, subsystem-specific boundaries.
- **User-facing docs** (`README.md`): installation, quickstart, config reference.

No `tests/` directory or `CONTRIBUTING.md` exist at time of writing. `pyproject.toml` configures `pytest` for a `tests/` directory that is absent, and `make test` references a missing `.coveragerc` (`Observed`).
