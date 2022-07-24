# -*- encoding: utf-8 -*-
# ! python3


from __future__ import annotations

import logging
import os
from functools import cache
from typing import List, Dict

import psycopg2

from downloader.downloader_utils.sql_commands import sql_get_products_command, sql_update_command

logger = logging.getLogger(__name__)


@cache
def db_connect() -> psycopg2.extensions.connection:
    """
    Crates connection to Postgres database.
    :return: connection client
    """
    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST"),
        port=os.environ.get("POSTGRES_PORT"),
        database=os.environ.get("DATABASE_NAME"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"))


def _get_all_products(cursor: psycopg2.extensions.cursor) -> List[str]:
    cursor.execute(sql_get_products_command)
    return [row[0] for row in cursor.fetchall()]


def database_product_fetching(cursor: psycopg2.extensions.cursor) -> List[str]:
    try:

        return _get_all_products(cursor=cursor)

    except Exception as e:
        logger.error(e)
        return []


def database_product_updating(postgres_connection: psycopg2.extensions.connection,
                              cursor: psycopg2.extensions.cursor,
                              product: str,
                              offer: Dict[str, str]):
    try:

        return update_offers(postgres_connection, cursor, product, offer)

    except Exception as e:
        print(e)
        return []


def update_offers(postgres_connection: psycopg2.extensions.connection,
                  cursor: psycopg2.extensions.cursor,
                  product: str,
                  offer: Dict[str, str]) -> None:
    _id = offer["id"]
    price = offer["price"]
    items_in_stock = offer["items_in_stock"]
    product_id = product

    cursor.execute(sql_update_command, (_id, price, items_in_stock, product_id, price, items_in_stock))
    postgres_connection.commit()
