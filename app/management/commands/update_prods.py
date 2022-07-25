# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import asyncio
import logging
import os
from typing import List, Final

import httpx
from asgiref.sync import sync_to_async
from django.core.management import BaseCommand
from django.db import transaction
from httpx import AsyncClient
from pydantic import PositiveInt
from tenacity import (
    after_log,
    before_log,
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_delay,
    wait_exponential,
)

from app.models import Product, Offer

logger = logging.getLogger(__name__)


@retry(
    reraise=True,
    before=before_log(logger, logging.DEBUG),
    after=after_log(logger, logging.INFO),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    wait=wait_exponential(multiplier=2, min=1, max=5),
    stop=stop_after_delay(30),
    retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TransportError)),
)
async def _download_product(client: AsyncClient, product_id: PositiveInt):
    """
    Download product from applift.
    :param client:
    :param product_id:
    :return:
    """
    logger.info(f"Downloading product {product_id}")
    response = await client.get(
        url=f"{os.environ.get('APPLIFT_BASE_URL').rstrip('/')}/products/{product_id}/offers")
    response.raise_for_status()
    logger.info(f"Downloaded product {product_id}")
    # [database_product_updating(product_id, item) for item in response.json()]

    return response.json()


@sync_to_async
def update_offers(product_id: PositiveInt, product_offers: List[dict]) -> bool:
    """
    Updates all offers.
    """
    logger.info(f"Updating offers for product {product_id}")
    try:
        with transaction.atomic():
            for product_offer in product_offers:
                Offer.objects.update_or_create(
                    id=product_offer["id"],
                    defaults={
                        "price": product_offer["price"],
                        "items_in_stock": product_offer["items_in_stock"],
                        "product": Product.objects.get(id=product_id),
                    }
                )
        logger.info(f"Updating offers for product {product_id} was successful")

        return True
    except Exception as e:
        logger.error(e)
        raise e


async def product_update(client: AsyncClient, product_id: PositiveInt):
    """
    Updates all products.
    :param client:
    :param products:
    :return:
    """
    new_product_offers = await _download_product(client, product_id)
    return await update_offers(product_id, new_product_offers)


async def _update_all_product_offers(products: List[int]):
    """
    Loops over all products and downloads them.
    :param client:
    :param products:
    :return:
    """
    headers: Final = {"Bearer": os.environ.get("SECRET_TOKEN")}

    async with httpx.AsyncClient(headers=headers) as client:
        content = await asyncio.gather(
            *(
                asyncio.create_task(product_update(client, product_offers))
                for product_offers in products
            )
        )
        return content


class Command(BaseCommand):
    help = 'Updates all offers'

    def _get_all_products(self) -> List[PositiveInt]:
        qs = Product.objects.all().values_list("id", flat=True)
        return list(qs)

    def handle(self, *args, **options):
        products: List[PositiveInt] = self._get_all_products()
        print(products)
        all_products = asyncio.run(_update_all_product_offers(products))
        print(all_products)
