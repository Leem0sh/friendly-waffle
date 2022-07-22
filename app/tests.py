# Create your tests here.


from app.db.operations import create_product, delete_product, get_product, update_product

from django.test import TestCase

from app.models import Product


class DatabaseTestCase(TestCase):
    def setUp(self) -> None:
        Product.objects.create(id="1", name="Product 1", description="Description 1")
        Product.objects.create(id="2", name="Product 2", description="Description 2")

    def test_create_product(self):
