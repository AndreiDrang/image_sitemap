import asyncio

from src.image_sitemap import Sitemap

asyncio.run(Sitemap(file_name="example_sitemap_images.xml").run(url="https://rucaptcha.com/", max_depth=1))
