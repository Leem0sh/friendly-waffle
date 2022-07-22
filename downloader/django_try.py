# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import asyncio
from typing import List

import httpx
from django.conf import settings
from django_cron import CronJobBase, Schedule

from app.models import Product


class Downloader(CronJobBase):
    RUN_EVERY_MINS = 5  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'applift.downloader'  # a unique code

    def _get_all_products(self):
        return Product.objects.all()

    def do(self):
        # TODO GET ALL IDS?

        products: List[Product] = self._get_all_products()
        print("hello")
        all_products = asyncio.run(_download_all_products(products))
        print(all_products)

        # TODO ASYNCIO GATHER?
        # TODO UPDATE DB?


async def _download_product(product_id):
    response = await httpx.AsyncClient().get(
        url=f"{settings.APPLIFT_BASE_URL.rstrip('/')}/products/{product_id}/offers")
    response.raise_for_status()
    return response.json()


async def _download_all_products(products):
    print("hello")

    content = await asyncio.gather(
        *(
            asyncio.create_task(_download_product(product.id))
            for product in products
        )
    )

    return content
