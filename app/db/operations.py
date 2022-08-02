# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from typing import Final, Dict, Tuple, List

from asgiref.sync import sync_to_async
from django.db import IntegrityError
from django.db.models import QuerySet
from pydantic import PositiveInt

from app.models import Product, Offer
from app.schemas import ProductSchema

logger: Final = logging.getLogger(__name__)


async def create_product(product: ProductSchema) -> bool:
    """
    Creates a new product.
    :param product:
    :return:
    """
    logger.info(f"Adding product {product.product_id} to database")
    try:
        _, created = await sync_to_async(Product.objects.get_or_create)(id=product.product_id,
                                                                        name=product.product_name,
                                                                        description=product.product_description)

        return created
    except Exception as e:
        logger.error(e)
        raise e


@sync_to_async
def delete_product(product_id: PositiveInt) -> Tuple[int, Dict[str, int]]:
    """
    Deletes a product.
    :param product_id:
    :return:
    """
    logger.info(f"Deleting product {product_id} from database")

    return Product.objects.get(id=product_id).delete()


@sync_to_async
def get_product(product_id: PositiveInt) -> Product | None:
    """
    Gets a product by its unique ID.
    :param product_id:
    :return:
    """
    logger.info(f"Getting product {product_id} from database")

    return Product.objects.get(id=product_id)


@sync_to_async
def get_all_products() -> List[QuerySet]:
    """
    Gets all products with all properties.
    :return:
    """
    logger.info("Getting all products from database")
    products = Product.objects.all().values()
    return list(products)


@sync_to_async
def update_product(product: ProductSchema) -> None:
    """
    Updates a product.
    :param product:
    :return: Returns true if the product was updated, false if the product was not found.
    """

    obj = Product.objects.get(id=product.product_id)
    obj.name = product.product_name
    obj.description = product.product_description
    logger.info(f"Updating product with ID={product.product_id} in database to {obj.name} | {obj.description}")
    obj.save()


@sync_to_async
def get_offers_for_product(product_id: str) -> List[QuerySet | QuerySet[Offer]]:
    """
    Get all offers for a product.
    :param product_id:
    :return:
    """
    logger.info(f"Getting offers for product {product_id} from database")
    try:
        offers = Offer.objects.all().filter(product_id=product_id).values()
    except IntegrityError as e:
        logger.error(e)
        raise e

    return list(offers)
