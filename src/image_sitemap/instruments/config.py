from typing import Set, Optional
from dataclasses import field, dataclass

__all__ = ("Config",)


@dataclass
class Config:
    """
    accept_subdomains: if True - crawlers will accept subdomains pages/links, else - No
    file_name: sitemap images file name
    exclude_file_links: if True - filter out file links from sitemap (recommended for SEO)
    allowed_file_extensions: set of file extensions to explicitly allow (None = use blacklist)
    excluded_file_extensions: set of file extensions to exclude from sitemap
    web_page_extensions: set of extensions that indicate web pages
    """

    max_depth: int = 1
    accept_subdomains: bool = True
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
