# -*- encoding: utf-8 -*-
# ! python3
from __future__ import annotations

from typing import List

from ninja import Schema
from pydantic import PositiveInt, constr, PositiveFloat
from pydantic.types import NonNegativeInt


class ProductSchema(Schema):
    product_id: PositiveInt
    product_name: constr(max_length=255)
    product_description: str


class OfferSchema(Schema):
    offer_id: PositiveInt
    offer_price: PositiveFloat
    offer_items_in_stock: NonNegativeInt


class OfferSchemas(Schema):
    offers: List[OfferSchema]


class RegisterResponseSchema(Schema):
    id: str


class RequestRecordCreatedSchema(Schema):
    name: str
