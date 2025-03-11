import urllib
import logging
from typing import Set

from .instruments import WebInstrument

logger = logging.getLogger(__name__)
__all__ = ("LinksCrawler",)


class LinksCrawler:
    def __init__(
        self, init_url: str, max_depth: int = 3, accept_subdomains: bool = True, is_query_enabled: bool = True
    ):
        self.max_depth = max_depth
        self.accept_subdomains = accept_subdomains
        self.is_query_enabled = is_query_enabled
        self.web_instrument = WebInstrument(init_url=init_url)

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
        if current_depth >= self.max_depth:
            return set()

        links = set()
        if page_data := await self.web_instrument.download_page(url=url):
            page_links = self.web_instrument.find_tags(page_data=page_data, tag="a", key="href")

            # filter only local weblinks
            inner_links = self.web_instrument.filter_inner_links(links=page_links)
            # filter global domain weblinks from local links
            links.update(
                self.web_instrument.filter_links_domain(
                    links=page_links.difference(inner_links),
                    is_subdomain=self.accept_subdomains,
                )
            )
            # create fixed inner links (fixed - added to local link page url)
            fixed_local_links = {urllib.parse.urljoin(url, inner_link) for inner_link in inner_links}

            # filter weblinks from webpages link minus links with query
            links.update(
                self.web_instrument.filter_links_query(links=fixed_local_links, is_query_enabled=self.is_query_enabled)
            )

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
        logger.info(
            f"Starting crawling - {self.web_instrument.init_url},"
            f" max depth - {self.max_depth},"
            f" with subdomains - {self.accept_subdomains},"
            f" with queries - {self.is_query_enabled}"
        )
        result = await self.__links_crawler(url=self.web_instrument.init_url)
        logger.info(f"Finishing crawling - {self.web_instrument.init_url}")
        return result
