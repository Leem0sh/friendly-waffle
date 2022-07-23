# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Final

import httpx
from django.conf import settings
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


# TODO what if call fails?
@retry(
    reraise=True,
    before=before_log(logger, logging.DEBUG),
    after=after_log(logger, logging.INFO),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_delay(timedelta(hours=1).total_seconds()),
    retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TransportError)),
)
async def register_new_product(product: ProductSchema) -> bool:
    """
    Registers a new product to offer MS.
    :param product:
    :return:
    """
    data = {
        "id": product.product_id,
        "name": product.product_name,
        "description": product.product_description,
    }
    try:

        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(
                url=f"{settings.APPLIFT_BASE_URL.rstrip('/')}/products/register",
                json=data,
                headers=get_headers()
            )
            if response.status_code == 201:
                logger.info(f"Registered product {product.product_id}")
                return True
            else:
                logger.warning(f"Failed to register product {product.product_id}")
                return False
    except Exception as e:
        logger.error(f"Failed to register product {product.product_id}")
        raise e
