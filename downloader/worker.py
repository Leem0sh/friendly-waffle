# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import asyncio
import logging
import os
from typing import Final

import dotenv
import httpx

from downloader.downloader_utils.db import database_product_fetching
from downloader.downloader_utils.http_connections import download_all_products

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADERS: Final = {"Bearer": os.environ.get("SECRET_TOKEN")}


async def main():
    """

    :return:
    """
    products = database_product_fetching()
    async with httpx.AsyncClient(headers=HEADERS) as client:
        content = await download_all_products(client, products)
    for p, c in zip(products, content):
        break


if __name__ == "__main__":
    asyncio.run(main())
