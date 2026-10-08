from django.test import TestCase

from store.models import Product


class ProductTests(TestCase):
    def test_slug_comes_from_the_title(self):
        product = Product.objects.create(title="Oak table", price="120.00")

        self.assertEqual(product.slug, "oak-table")

    def test_average_rating_is_zero_without_reviews(self):
        product = Product.objects.create(title="Oak table", price="120.00")

        self.assertEqual(product.average_rating(), 0)
