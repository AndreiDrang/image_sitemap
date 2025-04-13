import asyncio
from src.image_sitemap import Sitemap
from src.image_sitemap.instruments.config import Config

config = Config(
    max_depth=1,
    accept_subdomains=False,
    is_query_enabled=False,
    file_name="sitemap.xml",
    header={
        "User-Agent": "ImageSitemap Crawler",
        "Accept": "text/html",
    },
)

asyncio.run(Sitemap(config=config).run_images_sitemap(url="https://rucaptcha.com/"))
asyncio.run(Sitemap(config=config).run_sitemap(url="https://rucaptcha.com/"))
