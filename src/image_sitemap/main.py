import logging.config
from typing import Set, Dict

from .links_crawler import LinksCrawler
from .images_crawler import ImagesCrawler
from .instruments.config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)
__all__ = ("Sitemap",)


class Sitemap:
    def __init__(self, config: Config):
        """
        Main class for work with sitemap images generation

        In this class u can:
            1. Crawling website pages
            2. Generate sitemap images file or get this data
        Args:
            config: dataclass contains all params
        """
        self.config = config

    async def run_images_sitemap(self, url: str) -> None:
        """
        Basic images sitemap generation method
        1. Crawling webpages
        2. Creating images sitemap file
        Args:
            url: website address for crawling
        """
        logger.info(f"Run images sitemap command is started")
        links = await self.crawl_links(url=url)
        await self.generate_images_sitemap_file(links=links)
        logger.info(f"Run images sitemap command finished")

    async def generate_images_sitemap_file(self, links: Set[str]) -> None:
        """
        Method get webpages links set and collect images from them
        And finally generate images sitemap file

        Args:
            links: set with webpages links
        """
        logger.info(f"File generation started")
        images_crawler = ImagesCrawler(config=self.config)
        await images_crawler.create_sitemap(links=links)
        logger.info(f"File generation finished")

    async def images_data(self, links: Set[str]) -> Dict[str, Set[str]]:
        """
        Method collect and return images data as dictionary:
            key - webpage link
            values - set with webpage images
        Args:
            links: pages for parsing

        Returns:
            Dict with collected images data and pages
        """
        images_crawler = ImagesCrawler(config=self.config)
        return await images_crawler.get_data(links=links)

    async def crawl_links(self, url: str) -> Set[str]:
        """
        Method crawling website and collect all domain\subdomain pages
        Args:
            url: website page for starting crawling

        Returns:
            Set of all parsed website pages
        """
        logger.info(f"Pages crawling is started")
        return (await LinksCrawler(init_url=url, config=self.config).run()).crawled_links

    async def run_sitemap(self, url: str) -> None:
        """
        Basic images sitemap generation method
        1. Crawling webpages
        2. Creating images sitemap file
        Args:
            url: website address for crawling
        """
        logger.info(f"Run sitemap command is started")
        (await LinksCrawler(init_url=url, config=self.config).run()).create_sitemap()
        logger.info(f"Run sitemap command finished")
