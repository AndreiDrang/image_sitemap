# Agent Guidelines for image_sitemap

**Generated:** 2026-02-17  
**Commit:** 0a74998  
**Branch:** main  

## Overview
Async Python library for XML sitemap generation (website + image sitemaps). Crawls URLs, extracts images, outputs SEO-optimized XML.

## Structure
```
src/image_sitemap/
├── main.py              # Sitemap class - orchestrator entry point
├── links_crawler.py     # LinksCrawler - recursive page discovery
├── images_crawler.py    # ImagesCrawler - image URL extraction
├── __init__.py          # Exports: Sitemap, __version__
├── __version__.py       # Version string (2.1.0)
└── instruments/
    ├── config.py        # Config dataclass - 32 crawl settings
    ├── web.py           # WebInstrument - aiohttp HTTP (368 lines)
    ├── file.py          # FileInstrument - XML file generation
    └── templates.py     # XML template strings
```

## Where to Look
| Task | Location | Notes |
|------|----------|-------|
| Add crawl settings | `instruments/config.py` | Config dataclass (32 fields) |
| Modify HTTP behavior | `instruments/web.py` | WebInstrument class |
| Change XML output | `instruments/templates.py` | 5 template strings |
| Add sitemap features | `main.py` | Sitemap orchestrator (6 methods) |
| URL discovery logic | `links_crawler.py` | LinksCrawler (recursive) |
| Image extraction | `images_crawler.py` | ImagesCrawler (mime-type filter) |

## Code Map
| Symbol | Type | Location | Role |
|--------|------|----------|------|
| `Sitemap` | class | main.py:20 | Main entry, orchestrates crawling |
| `run_images_sitemap` | method | main.py:33 | Full image sitemap pipeline |
| `generate_images_sitemap_file` | method | main.py:46 | Generate from existing links |
| `images_data` | method | main.py:59 | Extract image data without saving |
| `crawl_links` | method | main.py:73 | Link discovery only |
| `run_sitemap` | method | main.py:86 | Standard sitemap (no images) |
| `LinksCrawler` | class | links_crawler.py:11 | Recursive URL discovery |
| `ImagesCrawler` | class | images_crawler.py:11 | Image URL extraction |
| `Config` | dataclass | instruments/config.py:7 | Crawl configuration (32 fields) |
| `WebInstrument` | class | instruments/web.py:17 | HTTP + HTML parsing (368 lines) |
| `FileInstrument` | class | instruments/file.py:14 | XML file generation |

## Conventions
- **Formatting**: Black 120-char, Python 3.12+
- **Imports**: isort black profile, use `__all__` exports
- **Types**: Full type hints, modern syntax (`dict[str, str]` not `Dict`)
- **Naming**: snake_case functions/variables, PascalCase classes
- **Docstrings**: Google style, required for public API
- **Async**: async/await with aiohttp, no sync HTTP calls
- **Config**: All settings via Config dataclass, never hardcode
- **Logging**: Use `logger = logging.getLogger(__name__)` - never print()

## Anti-Patterns
- No `as any`, `@ts-ignore` equivalents - fix type errors properly
- No empty exception handlers
- No hardcoded URLs/settings - use Config dataclass
- No sync HTTP - always aiohttp async
- No print() statements - use logging module

## Commands
```bash
make install    # pip install -e .
make refactor   # autoflake + black + isort (use before commit)
make lint       # Check formatting without changes
make test       # pytest with coverage
make build      # Build distribution
make upload     # Upload to PyPI
```

## Notes
- No tests directory exists yet (testpaths configured but empty)
- No CI/CD workflows - only Dependabot for dependency updates
- `build/lib/` is artifact - never edit, always edit `src/`
- Uses retry logic in WebInstrument (6 attempts with exponential backoff)
- Respects `rel="nofollow"` in link extraction
