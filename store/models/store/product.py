from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=500, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, related_name="products"
    )
    subcategory = models.ForeignKey(
        "Subcategory", on_delete=models.SET_NULL, null=True, related_name="products"
    )

    main_image = models.ImageField(upload_to="img/products/", blank=True, null=True)

    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    attributes = models.ManyToManyField(
        "AttributeValue", related_name="products", blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["price", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def average_rating(self):
        reviews = self.reviews.all()  # type: ignore
        if not reviews:
            return 0
        return sum(r.rating for r in reviews) / reviews.count()

    def clean(self):
        # Ensure subcategory belongs to the selected category
        if self.subcategory and self.category:
            if self.subcategory.category_id != self.category.id:
                raise ValidationError(
                    {
                        "subcategory": "Selected subcategory does not belong to the selected category."
                    }
                )
