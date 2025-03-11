import urllib
import mimetypes
from typing import Set, Dict

from .instruments import WebInstrument, FileInstrument

__all__ = ("ImagesCrawler",)


class ImagesCrawler:
    def __init__(self, file_name: str = "sitemap_images.xml", accept_subdomains: bool = True):
        if not file_name.endswith(".xml"):
            raise ValueError(f"File must be in XML format! Your file name - {file_name}")
        self.accept_subdomains = accept_subdomains
        self.file_instrument = FileInstrument(file_name=file_name)
        self.web_instrument = WebInstrument

    @staticmethod
    def __filter_images_links(links: Set[str]) -> Set[str]:
        result_links = set()
        for link in links:
            mime_type, _ = mimetypes.guess_type(link if link else "")
            if mime_type and mime_type.startswith("image/") and not link.startswith("data:image/"):
                result_links.add(link)
        return result_links

    async def __parse_images(self, url: str) -> Set[str]:
        links = set()
        if page_data := await self.web_instrument.download_page(url=url):
            images_links = self.__filter_images_links(
                links=self.web_instrument.find_tags(
                    page_data=page_data,
                    tag="img",
                    key="src",
                )
            )
            inner_links = self.web_instrument.filter_inner_links(links=images_links)
            links.update(
                self.web_instrument.filter_links_domain(
                    links=images_links.difference(inner_links), is_subdomain=self.accept_subdomains
                )
            )
            links.update({urllib.parse.urljoin(url, inner_link) for inner_link in inner_links})
        return links

    async def __prepare_images_struct(self, links: Set[str]) -> Dict[str, Set[str]]:
        images_data = dict()
        all_images = set()

        for url in sorted(links, key=len):
            if parsed_images := (await self.__parse_images(url=url)).difference(all_images):
                images_data.update({url: sorted(parsed_images, key=len)})
                all_images.update(parsed_images)

        return images_data

    async def create_sitemap(self, links: Set[str]):
        self.web_instrument = WebInstrument(init_url=next(iter(links)))
        self.file_instrument.create(links_images_data=await self.__prepare_images_struct(links=links))

    async def get_data(self, links: Set[str]) -> Dict[str, Set[str]]:
        self.web_instrument = WebInstrument(init_url=next(iter(links)))
        return await self.__prepare_images_struct(links=links)
