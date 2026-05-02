# AGENTS.md

## Repository Overview

Async Python library for XML sitemap generation (website + image sitemaps). Crawls URLs asynchronously, extracts images, outputs SEO-optimized XML files for search engine submission.

## Structure

```
src/image_sitemap/
├── main.py              # Sitemap orchestrator - primary entry point
├── links_crawler.py     # LinksCrawler - recursive URL discovery engine
├── images_crawler.py    # ImagesCrawler - image URL extraction with mime-type filtering
├── __init__.py          # Public API: Sitemap class, __version__
├── __version__.py       # Version string (2.1.0)
└── instruments/
    ├── config.py        # Config dataclass - 32 crawl settings
    ├── web.py           # WebInstrument - aiohttp HTTP client + BeautifulSoup parsing (368 lines)
    ├── file.py          # FileInstrument - XML file generation
    └── templates.py     # XML template strings for sitemap formats

scripts/
└── generate_tokenbel_sitemap.py  # Example usage script

files/
└── Logo.{png,svg}       # Project branding assets
```

## Where to Look

| Task | Location | Notes |
|------|----------|-------|
| Add crawl settings | `src/image_sitemap/instruments/config.py` | Config dataclass with 32 fields |
| Modify HTTP behavior | `src/image_sitemap/instruments/web.py` | aiohttp client, retry logic (6 attempts), BeautifulSoup parsing |
| Change XML output | `src/image_sitemap/instruments/templates.py` | 5 template strings for sitemap formats |
| Add sitemap features | `src/image_sitemap/main.py` | Sitemap orchestrator with 5 public methods |
| URL discovery logic | `src/image_sitemap/links_crawler.py` | Recursive crawler with depth control |
| Image extraction | `src/image_sitemap/images_crawler.py` | Mime-type filtering, duplicate prevention |

## Architecture and Boundaries

- **Single responsibility**: Each crawler class handles one type of extraction (links or images)
- **Instrument pattern**: WebInstrument (HTTP/parsing), FileInstrument (XML generation) are shared utilities
- **Async-first**: All I/O operations use async/await with aiohttp
- **No direct instantiation**: Always use `Sitemap` class as the public API entry point
- **Immutable crawlers**: Crawlers should not be modified after `run()` - create new instances

## Change Rules

- **Always use Config**: Never hardcode URLs, headers, or settings - use Config dataclass
- **Respect async**: Never use sync HTTP calls - always aiohttp
- **No print()**: Use `logger = logging.getLogger(__name__)` for all output
- **No regex for HTML**: Use BeautifulSoup for all HTML parsing
- **Preserve nofollow**: Respect `rel="nofollow"` in link extraction (already implemented in web.py:89-91)
- **Edit src/ only**: `build/lib/` is build artifact - never edit directly

## Validation

```bash
make lint       # black + isort + autoflake (check only)
make refactor   # autoflake + black + isort (apply changes)
make test       # pytest with coverage (requires .coveragerc which is missing)
```

## Commands

```bash
make install    # pip install -e .
make build      # Build distribution packages
make upload     # Upload to PyPI (requires twine)
```

## Conventions

- **Python**: 3.12+ only
- **Formatting**: Black 120-char line length
- **Imports**: isort with black profile, `__all__` exports required
- **Types**: Full type hints, modern syntax (`dict[str, str]` not `Dict`)
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Docstrings**: Google style, required for public API

## Anti-Patterns

- ❌ No `as any` or type ignoring - fix type errors properly
- ❌ No empty exception handlers
- ❌ No hardcoded URLs/settings/headers - use Config dataclass
- ❌ No sync HTTP - always aiohttp async (never `requests` library)
- ❌ No sync file I/O in async context - use `aiofiles` if needed
- ❌ No print() statements - use logging module
- ❌ No HTML parsing with regex - use BeautifulSoup
- ❌ No direct crawler instantiation - use `Sitemap` class
- ❌ No forgetting to `await` async methods
- ❌ No modifying crawlers after `run()` - create new instance

## Repository-Specific Gotchas

- **Retry logic**: WebInstrument uses exponential backoff with 6 attempts (web.py:357-367)
- **Subdomain handling**: Complex logic in web.py:147-203 for allowed/excluded subdomains
- **File filtering**: Extensive exclusion list in config.py:40-104 (100+ file extensions)
- **Mime-type filtering**: ImagesCrawler filters by mime-type prefix `image/` (images_crawler.py:23-24)
- **Missing .coveragerc**: Makefile references it but file doesn't exist
- **Missing tests/**: pyproject.toml configures pytest for `tests/` but directory doesn't exist
- **No CI/CD**: Only Dependabot configured for dependency updates

## Key Docs

- `README.md` - Usage examples and configuration options
- `pyproject.toml` - Project metadata, dependencies, tooling config
- `Makefile` - Development commands
