# AGENTS.md

## Scope

Shared utility layer for the image_sitemap library. Provides HTTP client/parsing, configuration, XML generation, and template strings. All crawlers depend on these instruments.

## What Lives Here

```text
instruments/
├── config.py        # Config dataclass — ~30 fields controlling crawl behavior
├── web.py           # WebInstrument — aiohttp HTTP client, HTML parsing, URL filtering (367 lines)
├── file.py          # FileInstrument — builds and writes XML sitemap files
└── templates.py     # XML template strings for sitemap and image-sitemap formats
```

## Local Boundaries and Invariants

- **WebInstrument is the sole HTTP layer**: All network requests go through `download_page()`. Never bypass it with raw aiohttp calls elsewhere.
- **Config is a frozen contract**: All behavioral tuning must flow through `Config` fields. Do not add ad-hoc parameters to instrument methods.
- **Templates are output contracts**: `templates.py` defines the XML structure that search engines expect. Changing these alters SEO compatibility — validate output against [Google's sitemap protocol](https://www.sitemaps.org/protocol.html).

## Safe Change Rules

- **web.py changes are high-risk**: It handles retry logic (exponential backoff, 6 attempts), subdomain filtering, nofollow exclusion, and URL normalization. Test thoroughly against real sites.
- **config.py field additions**: New fields must have sensible defaults — existing callers must not break.
- **templates.py**: Only modify if you understand the sitemap XML schema. Invalid XML breaks search engine ingestion.
- **file.py**: FileInstrument uses sync file I/O (standard `open()`). This is acceptable because it runs only after all async crawling completes, not inside an event loop.

## Validation

After changes to this subtree, run:

```bash
python example.py   # End-to-end smoke test — generates sitemap XML files
make lint           # Check formatting
```

## Nearby Docs

- Root `AGENTS.md` — project-wide conventions and architecture
- `README.md` — Config field descriptions and usage examples
