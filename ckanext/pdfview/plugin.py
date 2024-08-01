# encoding: utf-8

import logging
import ckan.plugins as p

log = logging.getLogger(__name__)
ignore_empty = p.toolkit.get_validator("ignore_empty")
url_validator = p.toolkit.get_validator("url_validator")


class PDFView(p.SingletonPlugin):
    """This plugin makes views of PDF resources, using an <object> tag"""

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IResourceView, inherit=True)

    def update_config(self, config):
        p.toolkit.add_template_directory(config, "theme/templates")

    def info(self):
        return {
            "name": "pdf_view",
            "title": p.toolkit._("PDF"),
            "icon": "file-pdf-o",
            "schema": {"pdf_url": [ignore_empty, url_validator]},
            "iframed": False,
            "always_available": False,
            "default_title": p.toolkit._("PDF"),
        }

    def can_view(self, data_dict):
        return data_dict["resource"].get("format", "").lower() == "pdf"

    def view_template(self, context, data_dict):
        
        def is_valid_domain(url):
            return url.startswith('https://data.dev-wins.com') or url.startswith('https://ihp-wins.unesco.org/')
        
        resource = data_dict["resource"]
        resource_view = data_dict["resource_view"]

        # Verifica si la URL necesita redirigirse al Blob Storage
        if is_valid_domain(resource["url"]):
            upload = p.toolkit.get_action('resource_uploader')(context, resource)
            resource_view['pdf_url'] = upload.get_url_from_filename(resource['id'], resource['url'])
        else:
            resource_view['pdf_url'] = resource.get("url")
                    
        return "pdf_view.html"

    def form_template(self, context, data_dict):
        return "pdf_form.html"
