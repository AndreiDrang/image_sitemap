from dataclasses import field, dataclass

__all__ = ("Config",)


@dataclass
class Config:
    """
    accept_subdomains: if True - crawlers will accept subdomains pages/links, else - No
    file_name: sitemap images file name
    """

    max_depth: int = 1
    accept_subdomains: bool = True
    is_query_enabled: bool = True
    file_name: str = "sitemap_images.xml"
    header: dict[str, str] = field(
        default_factory={
            "User-Agent": "ImageSitemap Crawler",
            "Accept": "text/html",
            "Accept-Encoding": "gzip",
            "Connection": "close",
        }
    )
