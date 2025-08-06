import asyncio
from image_sitemap import Sitemap
from image_sitemap.instruments.config import Config

images_config = Config(
    max_depth=3,
    accept_subdomains=True,
    is_query_enabled=False,
    file_name="sitemap_images.xml",
    header={
        "User-Agent": "ImageSitemap Crawler",
        "Accept": "text/html",
    },
)
sitemap_config = Config(
    max_depth=1,
    accept_subdomains=True,
    is_query_enabled=False,
    file_name="example_sitemap.xml",
    header={
        "User-Agent": "ImageSitemap Crawler",
        "Accept": "text/html",
    },
)

asyncio.run(Sitemap(config=images_config).run_images_sitemap(url="https://rucaptcha.com/"))
asyncio.run(Sitemap(config=sitemap_config).run_sitemap(url="https://rucaptcha.com/"))
