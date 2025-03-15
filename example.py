import asyncio

from src.image_sitemap import Sitemap
from src.image_sitemap.instruments.config import Config

config = Config(
    max_depth=1,
    accept_subdomains=True,
    is_query_enabled=False,
    file_name="example_sitemap_images.xml",
    header={
        "User-Agent": "ImageSitemap Crawler",
        "Accept": "text/html",
    },
)

asyncio.run(Sitemap(config=config).run(url="https://rucaptcha.com/"))
