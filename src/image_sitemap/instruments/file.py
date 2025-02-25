from typing import Set, Dict

from .templates import base_image_templ, base_loc_template, base_url_template, base_sitemap_templ

__all__ = ("FileInstrument",)


class FileInstrument:
    def __init__(self, file_name: str = "sitemap_images.xml"):
        self.file_name = file_name

    @staticmethod
    def __build_file(links_images_data: dict[str, Set[str]]):
        images_locs = []
        for link, images in links_images_data.items():
            loc = base_loc_template.format(link=link)
            for image_url in images:
                loc += base_image_templ.format(image_url=image_url)
            images_locs.append(base_url_template.format(loc=loc))

        return base_sitemap_templ.format(urls_data="".join(images_locs))

    def __save_file(self, file_data: str):
        with open(self.file_name, "wt") as file:
            file.write(file_data)

    def create(self, links_images_data: Dict[str, Set[str]]):
        file_data = self.__build_file(links_images_data=links_images_data)
        self.__save_file(file_data=file_data)
