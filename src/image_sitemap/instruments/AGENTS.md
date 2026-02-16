# Agent Guidelines for image_sitemap/instruments

**Generated:** 2026-02-17  
**Path:** src/image_sitemap/instruments/

## Overview
Supporting utilities for sitemap generation: HTTP client, XML generation, configuration, and templates.

## Structure
```
├── config.py        # Config dataclass - 32 fields for crawl settings
├── web.py           # WebInstrument - aiohttp + BeautifulSoup (368 lines)
├── file.py          # FileInstrument - XML file generation
├── templates.py     # XML template strings
└── __init__.py      # Exports: WebInstrument, FileInstrument
```

## Where to Look
| Task | Location | Notes |
|------|----------|-------|
| Add crawl settings | `config.py` | @dataclass with field defaults |
| Modify HTTP requests | `web.py` | `download_page()`, retry logic |
| Filter links | `web.py` | `filter_links()`, `filter_links_domain()` |
| Change XML format | `templates.py` | 5 template strings |
| Generate sitemap file | `file.py` | `create_sitemap()`, `create_image_sitemap()` |

## Code Map
| Symbol | Type | Location | Role |
|--------|------|----------|------|
| `Config` | dataclass | config.py:7 | 32-field configuration |
| `WebInstrument` | class | web.py:17 | HTTP client + link filtering |
| `download_page` | method | web.py:101 | Async page fetch with retries |
| `filter_links` | method | web.py:221 | Main link filtering pipeline |
| `find_tags` | method | web.py:67 | BeautifulSoup tag extraction |
| `FileInstrument` | class | file.py:14 | XML file writer |
| `create_sitemap` | method | file.py:95 | Standard XML sitemap |
| `create_image_sitemap` | method | file.py:83 | Image XML sitemap |

## Conventions
- **HTTP**: Use `WebInstrument` - never raw aiohttp
- **Retry**: Use `attempts_generator()` for consistency
- **Logging**: Always use `logger = logging.getLogger(__name__)`
- **Async**: All I/O methods must be async
- **Templates**: Raw XML strings in templates.py, not f-strings in code

## Anti-Patterns
- Never use `requests` library - aiohttp only
- Never use sync file I/O - use `aiofiles` if needed
- Never hardcode headers - use `Config.header`
- Never parse HTML with regex - use BeautifulSoup
