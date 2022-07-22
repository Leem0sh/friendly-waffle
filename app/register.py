# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import httpx
from django.conf import settings

from app.schemas import Product
from applift.auth import get_bearer


# TODO what if call fails?
def register_new_product(product: Product):
    data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
    }

    with httpx.Client() as http_client:
        response = http_client.post(
            url=f"{settings.APPLIFT_BASE_URL.rstrip('/')}/products/register",
            json=data,
            auth=get_bearer()
        )
        response.raise_for_status()
        return response.json()
