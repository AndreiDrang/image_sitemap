from typing import Dict, List

from .templates import (
    base_image_templ,
    base_loc_template,
    base_url_template,
    base_sitemap_templ,
    base_images_sitemap_templ,
)

__all__ = ("FileInstrument",)


class FileInstrument:
    def __init__(self, file_name: str):
        self.file_name = file_name

    @staticmethod
    def __build_image_sitemap_file(links_images_data: dict[str, List[str]]):
        images_locs = []
        for link, images in links_images_data.items():
            loc = base_loc_template.format(link=link)
            for image_url in images:
                loc += base_image_templ.format(image_url=image_url)
            images_locs.append(base_url_template.format(loc=loc))

        return base_images_sitemap_templ.format(urls_data="".join(images_locs))

    @staticmethod
    def __build_sitemap_file(links: List[str]):
        links_locs = []
        for link in links:
            loc = base_loc_template.format(link=link)
            links_locs.append(base_url_template.format(loc=loc))

        return base_sitemap_templ.format(urls_data="".join(links_locs))

    def __save_file(self, file_data: str):
        with open(self.file_name, "wt") as file:
            file.write(file_data)

    def create_image_sitemap(self, links_images_data: Dict[str, List[str]]):
        file_data = self.__build_image_sitemap_file(links_images_data=links_images_data)
        self.__save_file(file_data=file_data)

    def create_sitemap(self, links: List[str]):
        file_data = self.__build_sitemap_file(links=links)
        self.__save_file(file_data=file_data)
