# Agent Guidelines for image_sitemap (core)

**Generated:** 2026-02-17  
**Path:** src/image_sitemap/

## Overview
Core sitemap generation logic: orchestration, recursive link crawling, and image extraction.

## Structure
```
├── main.py              # Sitemap orchestrator - public API
├── links_crawler.py     # LinksCrawler - recursive page discovery
├── images_crawler.py    # ImagesCrawler - image extraction per page
├── __init__.py          # Package exports
└── __version__.py       # Version constant
```

## Where to Look
| Task | Location | Notes |
|------|----------|-------|
| Orchestrate full pipeline | `main.py` | `Sitemap` class with async methods |
| Recursive link discovery | `links_crawler.py` | `__links_crawler()` recursive method |
| Image extraction | `images_crawler.py` | `__parse_images()` per-page images |
| Entry points | `__init__.py` | `from .main import Sitemap` |

## Code Map
| Symbol | Type | Location | Role |
|--------|------|----------|------|
| `Sitemap` | class | main.py:20 | Main API - 6 public methods |
| `run_images_sitemap` | method | main.py:33 | Full pipeline: crawl → extract → save |
| `generate_images_sitemap_file` | method | main.py:46 | Skip crawl, use provided links |
| `images_data` | method | main.py:59 | Return dict, don't save |
| `crawl_links` | method | main.py:73 | Crawl only, no images |
| `run_sitemap` | method | main.py:86 | Standard sitemap, no images |
| `LinksCrawler` | class | links_crawler.py:11 | Recursive URL discovery |
| `LinksCrawler.run` | method | links_crawler.py:42 | Entry point for link crawling |
| `ImagesCrawler` | class | images_crawler.py:11 | Image extraction per page |
| `ImagesCrawler.create_sitemap` | method | images_crawler.py:58 | Generate image sitemap from links |

## Conventions
- **Entry**: Use `Sitemap` class from `main.py` - not crawlers directly
- **Async**: All crawler methods are async - await them
- **Config**: Pass `Config` instance to constructors
- **Links**: `LinksCrawler` produces `List[str]` for `ImagesCrawler`

## Anti-Patterns
- Don't instantiate crawlers directly - use `Sitemap` methods
- Don't mix link crawling with image extraction - separate concerns
- Don't forget to `await` crawler methods
- Don't modify crawlers after `run()` - create new instance
