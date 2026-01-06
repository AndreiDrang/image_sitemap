# Agent Guidelines for image_sitemap

**Generated:** 2026-01-07  


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
    ├── config.py        # Config dataclass - all crawl settings
    ├── web.py           # WebInstrument - aiohttp HTTP + BeautifulSoup parsing
    ├── file.py          # FileInstrument - XML file generation
    └── templates.py     # XML template strings
```

## Where to Look
| Task | Location | Notes |
|------|----------|-------|
| Add crawl settings | `instruments/config.py` | Config dataclass |
| Modify HTTP behavior | `instruments/web.py` | WebInstrument class |
| Change XML output | `instruments/templates.py` | Template strings |
| Add sitemap features | `main.py` | Sitemap orchestrator |
| URL discovery logic | `links_crawler.py` | LinksCrawler |
| Image extraction | `images_crawler.py` | ImagesCrawler |

## Code Map
| Symbol | Type | Location | Role |
|--------|------|----------|------|
| `Sitemap` | class | main.py | Main entry, orchestrates crawling |
| `LinksCrawler` | class | links_crawler.py | Recursive URL discovery |
| `ImagesCrawler` | class | images_crawler.py | Image URL extraction |
| `Config` | dataclass | instruments/config.py | Crawl configuration |
| `WebInstrument` | class | instruments/web.py | HTTP requests + HTML parsing |
| `FileInstrument` | class | instruments/file.py | XML file generation |

## Conventions
- **Formatting**: Black 120-char, Python 3.12+
- **Imports**: isort black profile, use `__all__` exports
- **Types**: Full type hints, modern syntax (`dict[str, str]` not `Dict`)
- **Naming**: snake_case functions/variables, PascalCase classes
- **Docstrings**: Google style, required for public API
- **Async**: async/await with aiohttp, no sync HTTP calls
- **Config**: All settings via Config dataclass, never hardcode

## Anti-Patterns
- No `as any`, `@ts-ignore` equivalents - fix type errors properly
- No empty exception handlers
- No hardcoded URLs/settings - use Config dataclass
- No sync HTTP - always aiohttp async

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
