from typing import Set

from .images_crawler import ImagesCrawler

__all__ = ("ImageSitemap",)


class ImageSitemap:
    def __init__(self, accept_subdomains: bool = True):
        """

        Args:
            accept_subdomains:
        """
        self.accept_subdomains = accept_subdomains

    async def generate_file(self, links: Set[str], file_name: str = "sitemap_images.xml") -> None:
        """

        Args:
            links:
            file_name:

        Returns:
            None
        """
        images_crawler = ImagesCrawler(file_name=file_name, accept_subdomains=self.accept_subdomains)
        await images_crawler.create_images_sitemap(links=links)

    async def get_url_images(self):
        pass

    async def crawl_links(self):
        pass
