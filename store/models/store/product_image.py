from django.db import models


class ProductImage(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="img/products/")
    alt = models.CharField(max_length=255, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.product.title} ({self.id})" # type: ignore
