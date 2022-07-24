# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Final

import httpx
from django.conf import settings
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

from app.schemas import ProductSchema
from applift.auth import get_headers

logger: Final = logging.getLogger(__name__)


# retry if http exc raised
@retry(
    reraise=True,
    before=before_log(logger, logging.DEBUG),
    after=after_log(logger, logging.INFO),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    wait=wait_exponential(multiplier=1, min=2, max=20),
    stop=stop_after_delay(timedelta(hours=1).total_seconds()),
    retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TransportError)),
)
async def register_new_product(http_client: AsyncClient, product: ProductSchema) -> bool:
    """
    Registers a new product to offer MS.

    :param http_client:
    :param product:
    :return:
    """
    data = {
        "id": product.product_id,
        "name": product.product_name,
        "description": product.product_description,
    }

    response = await http_client.post(
        url=f"{settings.APPLIFT_BASE_URL.rstrip('/')}/products/register",
        json=data,
        headers=get_headers()
    )
    logger.info(f"Processed register request with status {response.status_code} for product {product.product_id}")

    response.raise_for_status()
    logger.info(f"Registered product {product.product_id}")
    return True
