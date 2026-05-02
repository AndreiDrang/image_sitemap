# AGENTS.md

## Scope

Shared utility classes for the image_sitemap library. These instruments provide core functionality used across crawlers.

## What Lives Here

```
instruments/
├── config.py        # Config dataclass - 32 crawl settings for the entire library
├── web.py           # WebInstrument - aiohttp HTTP client + BeautifulSoup parsing (368 lines)
├── file.py          # FileInstrument - XML file generation from templates
└── templates.py     # XML template strings for sitemap formats
```

## Local Boundaries and Invariants

- **Config is immutable**: Once created, Config instances should not be modified
- **WebInstrument is stateless**: Each instance handles its own HTTP session lifecycle
- **Templates are pure**: Template strings contain no logic, only XML structure
- **FileInstrument writes sync**: Uses synchronous file I/O (acceptable for final output step)

## Safe Change Rules

- **Config changes**: Add new fields with sensible defaults; maintain backward compatibility
- **WebInstrument**: Preserve retry logic (6 attempts with exponential backoff)
- **Subdomain filtering**: Test changes against web.py:147-203 logic carefully
- **Templates**: Ensure generated XML validates against sitemap schemas
- **File I/O**: If adding async file operations, use `aiofiles` consistently

## Validation

- Changes to `config.py` should maintain all 32 existing fields
- Changes to `web.py` must preserve `rel="nofollow"` filtering (lines 89-91)
- Template changes must maintain XML namespace declarations

## Nearby Docs

- Parent: `src/image_sitemap/AGENTS.md` (if exists)
- Root: `AGENTS.md` for global conventions and anti-patterns
