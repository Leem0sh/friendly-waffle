# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import asyncio
import logging
import os
from typing import List

import httpx
from httpx import AsyncClient
from tenacity import (
    after_log,
    before_log,
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_delay,
    wait_exponential,
)

from downloader.downloader_utils.db import database_product_updating

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
async def _download_product(client: AsyncClient, postgres_connection, cursor, product_id: str):
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
    print(product_id, response.json())
    [database_product_updating(postgres_connection, cursor, product_id, item) for item in response.json()]

    return True


async def download_all_products(client: AsyncClient, postgres_connection, cursor, products: List[str]):
    """
    Loops over all products and downloads them.
    :param client:
    :param products:
    :return:
    """
    content = await asyncio.gather(
        *(
            asyncio.create_task(_download_product(client, postgres_connection, cursor, product))
            for product in products
        )
    )
    return content
