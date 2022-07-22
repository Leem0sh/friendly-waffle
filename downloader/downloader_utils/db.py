# -*- encoding: utf-8 -*-
# ! python3


from __future__ import annotations

import os
from functools import cache
from typing import List

import psycopg2


@cache
def db_connect() -> psycopg2.extensions.connection:
    """
    Crates connection to Postgres database.
    :return: connection client
    """
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"))


sql = "SELECT id FROM app_product"


def _get_all_products(cursor: psycopg2.extensions.cursor) -> List[str]:
    cursor.execute(sql)
    return [row[0] for row in cursor.fetchall()]


def database_fetching() -> List[str]:
    postgres_connection = None
    cursor = None
    try:
        postgres_connection = db_connect()
        cursor = postgres_connection.cursor()
        return _get_all_products(cursor=cursor)

    except Exception as e:
        print(e)
        return []
    finally:
        cursor.close()
        postgres_connection.close()
