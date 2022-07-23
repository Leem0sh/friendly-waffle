# -*- encoding: utf-8 -*-
# ! python3
from __future__ import annotations

from typing import List

from ninja import Schema
from pydantic import NonNegativeFloat
from pydantic.types import NonNegativeInt


# ContentChecksum: TypeAlias = constr(regex=r"^[a-fA-F0-9]{32}$", min_length=32, max_length=32)


class ProductSchema(Schema):
    product_id: str
    product_name: str
    product_description: str


class OfferSchema(Schema):
    offer_id: str
    offer_price: NonNegativeFloat
    offer_items_in_stock: NonNegativeInt


class OfferSchemas(Schema):
    offers: List[OfferSchema]


class RegisterResponseSchema(Schema):
    id: str


class RequestRecordCreatedSchema(Schema):
    name: str
