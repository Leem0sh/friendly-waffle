# -*- encoding: utf-8 -*-
# ! python3
from __future__ import annotations

from ninja import Schema
from pydantic import NonNegativeFloat, PositiveInt


class Product(Schema):
    id: str
    name: str
    description: str



class Offer(Schema):
    id: str
    price: NonNegativeFloat
    items_in_stock: PositiveInt
