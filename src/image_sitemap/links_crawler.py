import logging
from typing import Set

from .instruments import WebInstrument
from .instruments.config import Config

logger = logging.getLogger(__name__)
__all__ = ("LinksCrawler",)


class LinksCrawler:
    def __init__(self, init_url: str, config: Config):
        self.config = config
        self.web_instrument = WebInstrument(init_url=init_url, config=self.config)

    async def __links_crawler(self, url: str, current_depth: int = 0) -> Set[str]:
        """
        Method with recursion for webpages crawling
        Args:
            url: url for read and parse weblinks
            current_depth: current recursion depth
        Returns:
            Set of weblinks from page
        """
        logger.info(f"Crawling page - {url} , depth - {current_depth}")
        if current_depth >= self.config.max_depth:
            return set()

        links = set()
        if page_data := await self.web_instrument.download_page(url=url):
            page_links = self.web_instrument.find_tags(page_data=page_data, tag="a", key="href")
            links = self.web_instrument.filter_links(canonical_url=url, links=page_links)
            rec_parsed_links = set()
            for link in sorted(links, key=len):
                rec_parsed_links.update(await self.__links_crawler(url=link, current_depth=current_depth + 1))

            links.update(rec_parsed_links)

        return links

    async def run(self) -> Set[str]:
        """
        Method runs website crawling process
        Returns:
            Set with all crawled website pages links
        """
        logger.info(f"Starting crawling - {self.web_instrument.init_url}," f" config - {self.config}")
        result = await self.__links_crawler(url=self.web_instrument.init_url)
        logger.info(f"Finishing crawling - {self.web_instrument.init_url}")
        return result
