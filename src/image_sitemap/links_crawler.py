import urllib
import logging
from typing import Set

from .instruments import WebInstrument

logger = logging.getLogger(__name__)
__all__ = ("LinksCrawler",)


class LinksCrawler:
    def __init__(self, init_url: str, max_depth: int = 3, accept_subdomains: bool = True):
        self.max_depth = max_depth
        self.accept_subdomains = accept_subdomains
        self.web_instrument = WebInstrument(init_url=init_url)

    async def __links_crawler(self, url: str, current_depth: int = 0) -> Set[str]:
        logger.info(f"Crawling page - {url} , depth - {current_depth}")
        if current_depth >= self.max_depth:
            return set()

        links = set()
        if page_data := await self.web_instrument.download_page(url=url):
            page_links = self.web_instrument.find_tags(page_data=page_data, tag="a", key="href")

            inner_links = self.web_instrument.filter_inner_links(links=page_links)
            links.update(
                self.web_instrument.filter_links_domain(
                    links=page_links.difference(inner_links),
                    is_subdomain=self.accept_subdomains,
                )
            )
            links.update({urllib.parse.urljoin(url, inner_link) for inner_link in inner_links})

            rec_parsed_links = set()
            for link in links:
                rec_parsed_links.update(await self.__links_crawler(url=link, current_depth=current_depth + 1))

            links.update(rec_parsed_links)

        return links

    async def run(self) -> Set[str]:
        logger.info(
            f"Starting crawling - {self.web_instrument.init_url} , max depth - {self.max_depth} , with subdomains - {self.accept_subdomains}"
        )
        result = await self.__links_crawler(url=self.web_instrument.init_url)
        logger.info(f"Finishing crawling - {self.web_instrument.init_url}")
        return result
