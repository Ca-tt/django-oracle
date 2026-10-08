from django.db import models
from django.core.exceptions import ValidationError


# ? stored website data like site name, tagline, support email, etc.
class WebsiteConfig(models.Model):
    site_name = models.CharField(max_length=255, default="Zay")
    tagline = models.CharField(max_length=255, default="Gadgets that love you")
    support_email = models.EmailField(default="support@zaystore.com")
    contact_phone = models.CharField(max_length=20, default="0633216796")
    store_location = models.CharField(max_length=255, default="Ukraine, Kyiv, Khreshchatyk 1")
    #! test multilanguage features
    
    products_per_page = models.PositiveIntegerField(default=6)    

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    # ? only one instance editing allowed
    def save(self, *args, **kwargs):
        if not self.pk and WebsiteConfig.objects.exists():
            # Prevent creating a new one if one already exists
            raise ValidationError("There can be only one SiteConfig instance")
        return super().save(*args, **kwargs)
