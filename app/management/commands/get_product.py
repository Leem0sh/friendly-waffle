# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import asyncio
from typing import List

import httpx
from django.conf import settings
from django.core.management import BaseCommand

from app.models import Product


async def _download_product(product):
    response = await httpx.AsyncClient().get(
        url=f"{settings.APPLIFT_BASE_URL.rstrip('/')}/products/{product.id}/offers")
    response.raise_for_status()
    return response.json()


async def _download_all_products(products):
    content = await asyncio.gather(
        *(
            asyncio.create_task(_download_product(product.id))
            for product in products
        )
    )

    return content


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def _get_all_products(self):
        return Product.objects.all()

    def handle(self, *args, **options):
        products: List[Product] = self._get_all_products()
        all_products = asyncio.run(_download_all_products(products))
        print(all_products)
