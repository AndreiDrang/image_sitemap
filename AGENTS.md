# AGENTS.md

## Repository Overview

Async Python library for XML sitemap generation (website + image sitemaps). Crawls URLs asynchronously, extracts images, outputs SEO-optimized XML files for search engine submission. Published on PyPI as `image-sitemap`.

## Structure

```text
src/image_sitemap/
├── main.py              # Sitemap class — public API entry point, orchestrates crawlers
├── links_crawler.py     # LinksCrawler — recursive URL discovery with depth control
├── images_crawler.py    # ImagesCrawler — image extraction with mime-type filtering
├── __init__.py          # Exports: Sitemap, __version__
├── __version__.py       # Version string
└── instruments/
    ├── config.py        # Config dataclass — all crawl settings
    ├── web.py           # WebInstrument — aiohttp HTTP client + BeautifulSoup parsing
    ├── file.py          # FileInstrument — XML file generation
    └── templates.py     # XML template strings for sitemap formats

example.py               # Runnable example that crawls rucaptcha.com
files/                   # Project branding assets (Logo.png, Logo.svg)
```

## Where to Look

| Task | Location | Notes |
|------|----------|-------|
| Add crawl settings | `instruments/config.py` | Config dataclass with ~30 fields |
| Modify HTTP behavior | `instruments/web.py` | aiohttp client, retry logic, BeautifulSoup parsing |
| Change XML output | `instruments/templates.py` + `instruments/file.py` | Templates define XML structure, FileInstrument writes files |
| Add sitemap features | `main.py` | Sitemap class with 5 public methods |
| URL discovery logic | `links_crawler.py` | Recursive BFS crawler with depth control |
| Image extraction | `images_crawler.py` | Mime-type filtering, data-URI exclusion |

## Architecture and Boundaries

- **Public API surface**: `Sitemap` class in `main.py` — all consumers use this
- **Instrument pattern**: `WebInstrument` (HTTP/parsing), `FileInstrument` (XML generation) are shared utilities injected into crawlers
- **Single-responsibility crawlers**: `LinksCrawler` discovers URLs, `ImagesCrawler` extracts images — never mix responsibilities
- **Async-first**: All I/O uses async/await with aiohttp; no sync HTTP anywhere
- **Immutable crawlers**: Do not modify crawler state after `run()` — create new instances
- **Config-driven**: All behavior tunable through `Config` dataclass, never hardcoded

## Change Rules

- **Always use Config**: Never hardcode URLs, headers, timeouts, or settings
- **Never use sync HTTP**: Always aiohttp; `requests` library is forbidden
- **No print()**: Use `logger = logging.getLogger(__name__)`
- **No regex for HTML**: Use BeautifulSoup for all HTML parsing
- **Preserve nofollow**: `rel="nofollow"` links must be excluded (`web.py:89-91`)
- **Edit `src/` only**: `build/lib/` is a build artifact

## Validation

```bash
make lint       # black + isort + autoflake (check only)
make refactor   # autoflake + black + isort (apply changes)
```

Note: `make test` is defined but requires a missing `.coveragerc` and `tests/` directory. No tests currently exist.

## Commands

```bash
make install    # pip install -e .
make build      # python3 -m build
make upload     # twine upload dist/*
```

## Conventions

- **Python**: 3.12+ only, modern type syntax (`dict[str, str]` not `Dict`)
- **Formatting**: Black 120-char line length
- **Imports**: isort with black profile; `__all__` exports required
- **Docstrings**: Google style, required for public API

## Anti-Patterns

- No `as any` or type ignoring — fix type errors properly
- No empty exception handlers
- No sync file I/O in async context — use `aiofiles` if needed
- No HTML parsing with regex — use BeautifulSoup
- No direct crawler instantiation — use `Sitemap` class
- No forgetting to `await` async methods
- No modifying crawlers after `run()` — create new instance

## Repository-Specific Gotchas

- **Retry logic**: `WebInstrument.attempts_generator` yields attempt numbers for retry loop (`web.py:357-367`), used with exponential backoff
- **Subdomain filtering**: `is_subdomain_excluded` and `filter_links_domain` handle allowed/excluded subdomains (`web.py:147-203`)
- **File extension exclusion**: `excluded_file_extensions` in config blocks ~60 file extensions from crawling (`config.py:40-104`)
- **Mime-type image filtering**: `ImagesCrawler.__filter_images_links` uses `mimetypes.guess_type` + `image/` prefix check, excludes data URIs (`images_crawler.py:20-26`)
- **Missing tests/**: `pyproject.toml` configures pytest for `tests/` but the directory does not exist
- **Missing .coveragerc**: Makefile test target references it but the file does not exist
- **No CI/CD**: Only Dependabot configured (`.github/dependabot.yml`)

## Key Docs

- `README.md` — Usage examples and configuration options
- `pyproject.toml` — Project metadata, dependencies, tooling config
- `Makefile` — Development commands
- `instruments/AGENTS.md` — Local rules for the instruments subsystem
