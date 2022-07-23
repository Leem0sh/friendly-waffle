# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import asyncio
import logging
import os
from typing import Final

import dotenv
import httpx

from downloader.downloader_utils.db import db_connect, database_product_fetching
from downloader.downloader_utils.http_connections import download_all_products
from downloader.downloader_utils.setups import setup_logging

dotenv.load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)

HEADERS: Final = {"Bearer": os.environ.get("SECRET_TOKEN")}


async def main():
    """

    :return:
    """
    postgres_connection = db_connect()
    cursor = postgres_connection.cursor()

    try:
        products = database_product_fetching(cursor)
        async with httpx.AsyncClient(headers=HEADERS) as client:
            await download_all_products(client, postgres_connection, cursor, products)

    except Exception as e:
        logger.error(e)
        raise e

    finally:
        cursor.close()
        postgres_connection.close()
        logger.info("Finished")


if __name__ == "__main__":
    asyncio.run(main())
