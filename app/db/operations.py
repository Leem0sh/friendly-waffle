# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from typing import Final, Dict, Tuple, List

from asgiref.sync import sync_to_async
from django.db.models import QuerySet

from app.models import Product, Offer
from app.schemas import ProductSchema

logger: Final = logging.getLogger(__name__)


async def create_product(product: ProductSchema) -> bool:
    """
    Creates a new product.
    :param product:
    :return:
    """
    try:
        _, created = await sync_to_async(Product.objects.get_or_create)(id=product.product_id,
                                                                        name=product.product_name,
                                                                        description=product.product_description)

        return created
    except Exception as e:
        logger.error(e)
        raise e


@sync_to_async
def delete_product(product_id: str) -> Tuple[int, Dict[str, int]]:
    """
    Deletes a product.
    :param product_id:
    :return:
    """
    return Product.objects.all().filter(id=product_id).delete()


@sync_to_async
def get_product(product_id: str) -> Product:
    """
    Gets a product by its unique ID.
    :param product_id:
    :return:
    """
    return Product.objects.all().filter(id=product_id).first()


@sync_to_async
def update_product(product: ProductSchema) -> bool:
    """
    Updates a product.
    :param product:
    :return:
    """
    obj = Product.objects.all().filter(id=product.product_id).first()
    if obj:
        obj.name = product.product_name
        obj.description = product.product_description
        obj.save()
        return True
    return False


@sync_to_async
def get_offers(product_id: str) -> List[QuerySet | QuerySet[Offer]]:
    """
    Get all offers for a product.
    :param product_id:
    :return:
    """
    offers = Offer.objects.all().filter(product_id=product_id).values()
    return list(offers)
