from typing import Set, Optional
from dataclasses import field, dataclass

__all__ = ("Config",)


@dataclass
class Config:
    """Configuration class for sitemap generation parameters.

    Attributes:
        max_depth: Maximum crawling depth for website pages. Defaults to 1.
        accept_subdomains: If True, crawlers will accept subdomain pages/links.
            If False, only the main domain is crawled. Defaults to True.
        excluded_subdomains: Set of subdomain names to exclude from parsing
            (e.g., {"blog", "api", "staging"}). Defaults to empty set.
        is_query_enabled: If True, URLs with query parameters are included
            in sitemap. Defaults to True.
        file_name: Output sitemap file name. Defaults to "sitemap_images.xml".
        exclude_file_links: If True, filter out file links from sitemap
            (recommended for SEO). Defaults to True.
        allowed_file_extensions: Set of file extensions to explicitly allow.
            If None, uses blacklist mode. Defaults to None.
        excluded_file_extensions: Set of file extensions to exclude from sitemap
            when in blacklist mode. Defaults to comprehensive file type list.
        web_page_extensions: Set of extensions that indicate web pages rather
            than downloadable files. Defaults to common web extensions.
        header: Dictionary of HTTP headers to use for requests. Defaults to
            standard crawler headers.
    """

    max_depth: int = 1
    accept_subdomains: bool = True
    excluded_subdomains: Set[str] = field(default_factory=set)
    is_query_enabled: bool = True
    file_name: str = "sitemap_images.xml"
    exclude_file_links: bool = True
    allowed_file_extensions: Optional[Set[str]] = None
    excluded_file_extensions: Set[str] = field(
        default_factory=lambda: {
            # Documents
            ".pdf",
            ".doc",
            ".docx",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
            ".rtf",
            ".txt",
            # Media files
            ".mp4",
            ".mp3",
            ".avi",
            ".mov",
            ".wmv",
            ".flv",
            ".webm",
            ".mkv",
            ".m4v",
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".webp",
            ".svg",
            ".ico",
            ".bmp",
            ".tiff",
            # Compressed files
            ".zip",
            ".rar",
            ".7z",
            ".tar",
            ".gz",
            ".bz2",
            # Code/Resource files
            ".css",
            ".js",
            ".xml",
            ".json",
            ".yml",
            ".yaml",
            ".ini",
            ".cfg",
            ".conf",
            # Executables
            ".exe",
            ".msi",
            ".dmg",
            ".deb",
            ".rpm",
            ".app",
            ".pkg",
            # Other common files
            ".csv",
            ".sql",
            ".db",
            ".log",
            ".tmp",
            ".bak",
        }
    )
    web_page_extensions: Set[str] = field(
        default_factory=lambda: {".html", ".htm", ".php", ".aspx", ".jsp", ".asp", ".cfm", ".pl", ".py"}
    )
    header: dict[str, str] = field(
        default_factory=lambda: {
            "User-Agent": "ImageSitemap Crawler",
            "Accept": "text/html",
            "Accept-Encoding": "gzip",
            "Connection": "close",
        }
    )
