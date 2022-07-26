# Create your tests here.


from django.test import TestCase

from app.db.operations import create_product, delete_product, get_product, update_product, get_offers_for_product
from app.models import Product, Offer
from app.schemas import ProductSchema


class DatabaseTestCase(TestCase):
    def setUp(self) -> None:
        Product.objects.create(id=1, name="Product 1", description="Description 1")
        Product.objects.create(id=2, name="Product 2", description="Description 2")
        Offer.objects.create(id=123456, price=123, items_in_stock=132, product_id="1")

    async def test_create_product(self):
        product = ProductSchema(product_id=3, product_name="Product 3", product_description="Description 3")
        created = await create_product(product=product)
        self.assertTrue(created)
        created = await create_product(product=product)
        self.assertFalse(created)

    async def test_get_product(self):
        product = await get_product(product_id=1)
        self.assertEqual(product.id, 1)

    async def test_update_product(self):
        product = ProductSchema(product_id=1, product_name="Product XX", product_description="Descrrrr")
        await update_product(product=product)
        updated_data = await get_product(product_id=1)
        self.assertEqual(updated_data.id, 1)
        self.assertEqual(updated_data.name, "Product XX")
        self.assertEqual(updated_data.description, "Descrrrr")

    async def test_get_offers_for_product(self):
        offers = await get_offers_for_product(product_id=1)
        self.assertEqual(len(offers), 1)

    async def test_delete_product(self):
        deleted = await delete_product(product_id=1)
        self.assertEqual(deleted, (2, {'app.Offer': 1, 'app.Product': 1}))
