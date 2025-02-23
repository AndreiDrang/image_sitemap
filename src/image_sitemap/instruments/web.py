import asyncio
import logging
from typing import Set, Optional
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup

__all__ = ("WebInstrument",)


def attempts_generator(amount: int = 5) -> int:
    """
    Function generates a generator of length equal to `amount`

    Args:
        amount: number of attempts generated

    Returns:
        Attempt number
    """
    yield from range(1, amount)


class WebInstrument:
    def __init__(self, init_url: str):
        self.init_url = init_url
        self.domain = self.get_domain(url=self.init_url)

    @staticmethod
    def get_domain(url: str) -> str:
        return ".".join(urlparse(url=url).hostname.split(".")[-2:])

    @staticmethod
    def find_tags(page_data: str, tag: str, key: str) -> Set[str]:
        result_images = set()
        soup = BeautifulSoup(page_data)
        images = soup.find_all(tag)
        for image in images:
            result_images.add(image.get(key))
        return result_images

    @staticmethod
    async def download_page(url: str) -> Optional[str]:
        async with aiohttp.ClientSession() as session:
            for attempt in attempts_generator():
                try:
                    async with session.get(url=url) as resp:
                        if resp.status == 429:
                            await asyncio.sleep(1 * attempt)
                            raise ValueError(
                                f"Too many requests {attempt = }, {url = } ; {resp.status = }, {await resp.text()}"
                            )
                        return await resp.text()
                except Exception as err:
                    logging.warning(f"{err}")
            else:
                logging.error(f"Page not loaded - {url = }")

    def filter_links_domain(self, links: Set[str], is_subdomain: bool = True) -> Set[str]:
        result_links = set()
        check_logic = "endswith" if is_subdomain else "__eq__"
        for link in links:
            link_domain = urlparse(url=link).hostname
            if link_domain and getattr(link_domain, check_logic)(self.domain):
                result_links.add(link)
        return result_links

    @staticmethod
    def filter_inner_links(links: Set[str]) -> Set[str]:
        result_links = set()
        for link in links:
            if link and not link.startswith("https://"):
                result_links.add(link)
        return result_links
