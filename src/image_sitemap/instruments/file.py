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
    """Instrument for creating and saving XML sitemap files.
    
    Handles the generation of both standard sitemaps and image sitemaps,
    formatting the data according to XML sitemap standards and saving
    them to specified files.
    """
    
    def __init__(self, file_name: str):
        """Initialize FileInstrument with target file name.
        
        Args:
            file_name: Name of the file where sitemap will be saved.
        """
        self.file_name = file_name

    @staticmethod
    def __build_image_sitemap_file(links_images_data: dict[str, List[str]]) -> str:
        """Build XML content for image sitemap.
        
        Creates XML sitemap content that includes both page URLs and
        their associated image URLs according to sitemap image protocol.
        
        Args:
            links_images_data: Dictionary mapping page URLs to lists of image URLs.
            
        Returns:
            Formatted XML string for the image sitemap.
        """
        images_locs = []
        for link, images in links_images_data.items():
            loc = base_loc_template.format(link=link)
            for image_url in images:
                loc += base_image_templ.format(image_url=image_url)
            images_locs.append(base_url_template.format(loc=loc))

        return base_images_sitemap_templ.format(urls_data="".join(images_locs))

    @staticmethod
    def __build_sitemap_file(links: List[str]) -> str:
        """Build XML content for standard sitemap.
        
        Creates XML sitemap content containing only page URLs
        according to standard sitemap protocol.
        
        Args:
            links: List of page URLs to include in the sitemap.
            
        Returns:
            Formatted XML string for the standard sitemap.
        """
        links_locs = []
        for link in links:
            loc = base_loc_template.format(link=link)
            links_locs.append(base_url_template.format(loc=loc))

        return base_sitemap_templ.format(urls_data="".join(links_locs))

    def __save_file(self, file_data: str) -> None:
        """Save XML content to file.
        
        Writes the provided XML data to the specified file name.
        
        Args:
            file_data: XML content to be written to file.
        """
        with open(self.file_name, "wt") as file:
            file.write(file_data)

    def create_image_sitemap(self, links_images_data: Dict[str, List[str]]) -> None:
        """Create and save an image sitemap file.
        
        Generates XML sitemap with images and saves it to the file
        specified during initialization.
        
        Args:
            links_images_data: Dictionary mapping page URLs to lists of image URLs.
        """
        file_data = self.__build_image_sitemap_file(links_images_data=links_images_data)
        self.__save_file(file_data=file_data)

    def create_sitemap(self, links: List[str]) -> None:
        """Create and save a standard sitemap file.
        
        Generates XML sitemap without images and saves it to the file
        specified during initialization.
        
        Args:
            links: List of page URLs to include in the sitemap.
        """
        file_data = self.__build_sitemap_file(links=links)
        self.__save_file(file_data=file_data)
