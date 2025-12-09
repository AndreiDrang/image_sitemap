# Agent Guidelines for image_sitemap

## Project Overview
**image_sitemap** - Image & Website Sitemap Generator - SEO Tool for Better Visibility

Library to generate XML sitemaps for websites and images. Boosts SEO by indexing image URLs for better visibility on search engines (Google, Bing, Yahoo). Supports both website and image sitemap generation, easy integration with Python projects, and helps improve search engine results visibility.

**Framework:** AsyncIO, Python 3.12+  
**Stack:** aiohttp, beautifulsoup4, black, isort, autoflake

## Lint Commands
- `make refactor` - Auto-format code (autoflake, black, isort)

## Code Style Guidelines
- **Formatting**: Black with 120-line length, Python 3.12+
- **Imports**: isort with black profile, use `__all__` exports
- **Types**: Full type hints required, use modern syntax (dict[str, str])
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Error Handling**: Use specific exceptions (e.g., `ValueError` with descriptive messages)
- **Logging**: Use `logging.getLogger(__name__)` with INFO level
- **Documentation**: Comprehensive docstrings explaining methods and parameters
- **Async**: Use async/await patterns with aiohttp for HTTP requests
- **Structure**: PlaceConfig dataclass in `instruments/config.py` for configuration

## Package Structure
- Main code in `src/image_sitemap/`
- Configuration via `Config` dataclass in `instruments/config.py`
- Web crawling in `instruments/web.py`, file operations in `instruments/file.py`
- Use relative imports within package (`from .module import Class`)

### Docstring Policy
- **Style**: Google Python docstring style is **required** for modules, public classes, public functions/method.
- **Python docstrings**: for docstrings in python classes, methods, functions also use PEP 257.
- **Required for**:
  - Public functions and methods
  - Public classes
