import asyncio
import logging
from typing import Set, Optional
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

__all__ = ("WebInstrument",)


class WebInstrument:
    def __init__(self, init_url: str):
        """
        Core class for working with webpages:

        1. get webpages

        2. get webpage tags

        3. filter links

        Args:
            init_url: webpage main link
        """
        self.init_url = init_url
        self.domain = self.get_domain(url=self.init_url)
        self.headers = {
            "User-Agent": "ImageSitemap Crawler",
            "Accept": "text/html",
            "Accept-Encoding": "gzip",
            "Connection": "close",
        }

    @staticmethod
    def get_domain(url: str) -> str:
        """
        Method parse link to get core domain from it
        Args:
            url: webpage link

        Returns:
            domain name
        """
        return ".".join(urlparse(url=url).hostname.split(".")[-2:])

    @staticmethod
    def find_tags(page_data: str, tag: str, key: str) -> Set[str]:
        """
        Method parse webpage text and extract certain tags and keys
        Args:
            page_data: downloaded webpage text
            tag: tag for parsing
            key: tag key for extract

        Returns:
            Set of all extracted tag keys values
        """
        result_images = set()
        soup = BeautifulSoup(page_data)
        images = soup.find_all(tag)
        for image in images:
            result_images.add(image.get(key))
        return result_images

    async def download_page(self, url: str) -> Optional[str]:
        """
        Method connect open webpage and download it's as text
        Args:
            url: webpage for downloading

        Returns:
            Webpage as text
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            for attempt in self.attempts_generator():
                try:
                    async with session.get(url=url) as resp:
                        if resp.status == 200:
                            logger.info(f"Page success loaded - {url = }")
                            return await resp.text()
                        else:
                            await asyncio.sleep(1 * attempt)
                            raise ValueError(
                                f"Wrong response status {attempt = }, {url = } ; {resp.status = }, {await resp.text()}"
                            )
                except Exception as err:
                    logger.warning(f"{err}")
            else:
                logger.error(f"Page not loaded - {url = }")

    @staticmethod
    def filter_links_query(links: Set[str], is_query_enabled: bool = True) -> Set[str]:
        """
        Method filter webpages links set and return only links with same domain or subdomain
        Args:
            links: set of links for filtering
            is_query_enabled: accept or not links with query strings

        Returns:
            Filtered list of links
        """
        result_links = set()
        for link in links:
            if is_query_enabled and urlparse(url=link).query:
                result_links.add(link)
            elif not urlparse(url=link).query:
                result_links.add(link)
        return result_links

    def filter_links_domain(self, links: Set[str], is_subdomain: bool = True) -> Set[str]:
        """
        Method filter webpages links set and return only links with same domain or subdomain
        Args:
            links: set of links for filtering
            is_subdomain: accept or not links with subdomain

        Returns:
            Filtered list of links
        """
        result_links = set()
        check_logic = "endswith" if is_subdomain else "__eq__"
        for link in links:
            link_domain = urlparse(url=link).hostname
            if link_domain and getattr(link_domain, check_logic)(self.domain):
                result_links.add(link)
        return result_links

    @staticmethod
    def filter_inner_links(links: Set[str]) -> Set[str]:
        """
        Method get set of links and filter them from non-inner website links
        Args:
            links: set of website links

        Returns:
            Filtered list of links only with inner links
        """
        result_links = set()
        for link in links:
            if link and not link.startswith("https://"):
                result_links.add(link)
        return result_links

    @staticmethod
    def attempts_generator(amount: int = 6) -> int:
        """
        Function generates a generator of length equal to `amount`

        Args:
            amount: number of attempts generated

        Returns:
            Attempt number
        """
        yield from range(1, amount)
