from dataclasses import dataclass

@dataclass
class WebsiteConfigScheme:
    id: str = "id"
    site_name: str = "site_name"
    tagline: str = "tagline"
    support_email: str = "support_email"
    contact_phone: str = "contact_phone"
    

@dataclass
class WebsiteSettings:
    website_config: str = "website_config"
    admin_url: str = "control/"
    admin_url_redirect: str = "cc/"
    social_media_links: str = "social_media_links"