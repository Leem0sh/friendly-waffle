# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from typing import Final, Dict, Tuple, List

from asgiref.sync import sync_to_async
from django.db import IntegrityError

from app.models import Product, Offer
from app.schemas import ProductSchema

logger: Final = logging.getLogger(__name__)


async def create_product(product: ProductSchema) -> bool:
    try:
        await sync_to_async(Product.objects.create)(id=product.product_id,
                                                    name=product.product_name,
                                                    description=product.product_description)
        return True
    except IntegrityError:
        return False


@sync_to_async
def delete_product(product_id: str) -> Tuple[int, Dict[str, int]]:
    return Product.objects.all().filter(id=product_id).delete()


@sync_to_async
def get_product(product_id: str) -> Product:
    return Product.objects.all().filter(id=product_id).first()


@sync_to_async
def update_product(product: ProductSchema) -> bool:
    obj = Product.objects.all().filter(id=product.product_id).first()
    if obj:
        obj.name = product.product_name
        obj.description = product.product_description
        obj.save()
        return True
    return False


@sync_to_async
def get_offers(product_id: str) -> List[Offer]:
    offers = Offer.objects.all().filter(product_id=product_id).values()

    return list(offers)
