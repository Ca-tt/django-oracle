from unicodedata import category
from django.db import models
from django.utils.text import slugify
from django.apps import apps


class Subcategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="subcategories"
    )

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            Product = apps.get_model("store", "Product")
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
