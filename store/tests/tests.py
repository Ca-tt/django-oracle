from http import HTTPStatus
from typing import cast

from django.http import HttpResponse
from django.test import TestCase

from store.models import Product, Subcategory
from store.tests.seed import seed_categories


class StoreTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        seed_categories()


class HomePageTests(StoreTestCase):
    def test_home_returns_200(self):
        response = cast(HttpResponse, self.client.get("/"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class ProductsPageTests(StoreTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        tables = Subcategory.objects.get(name="Tables")
        cls.product = Product.objects.create(
            title="Oak table",
            price="120.00",
            category=tables.category,
            subcategory=tables,
        )

    def test_product_uses_seeded_subcategory(self):
        self.assertEqual(self.product.subcategory.name, "Tables")
