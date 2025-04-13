base_images_sitemap_templ = """<?xml version="1.0" encoding="UTF-8"?>
<urlset
\txmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
\txmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
{urls_data}</urlset>\n"""

base_image_templ = """\t\t<image:image>
\t\t\t<image:loc>{image_url}</image:loc>
\t\t</image:image>
"""
base_loc_template = """\t\t<loc>{link}</loc>\n"""
base_url_template = """\t<url>\n{loc}\t</url>\n"""

base_sitemap_templ = """<?xml version="1.0" encoding="UTF-8"?>
<urlset
\txmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls_data}</urlset>\n"""
