# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from http import HTTPStatus
from typing import Final

import httpx
from django.http import HttpRequest, JsonResponse
from ninja import NinjaAPI
from ninja.errors import HttpError
from pydantic import PositiveInt

from app.api_auth import AuthBearer
from app.db.operations import create_product, delete_product, get_product, update_product, get_offers
from app.models import Product
from app.register import register_new_product
from app.schemas import ProductSchema

logger: Final = logging.getLogger(__name__)

api: Final = NinjaAPI(title="Applift JSON API", version="0.1.0", urls_namespace="applift-api")


@api.post(
    "/create-product",
    summary="Creates a new product",
    description="Creates a new product and registers it to the Offer MS.",
    operation_id="create_product",
    tags=["Products"],
    auth=AuthBearer(),
)
async def _(
        request: HttpRequest,
        product: ProductSchema,
) -> JsonResponse:
    """
    Creates a new product.
    :param request:
    :param product:
    :return:
    """
    logger.info(f"Processing API request {request.method}")
    created = await create_product(product=product)
    if not created:
        logger.warning(f"Product {product.product_id} already exists")
        raise HttpError(
            status_code=HTTPStatus.CONFLICT, message="This record already exists."
        )
    try:
        async with httpx.AsyncClient() as http_client:
            await register_new_product(http_client=http_client, product=product)
    except (httpx.HTTPStatusError, httpx.TransportError):
        logger.error(f"Product {product.product_id} created in database but not registered")
        await delete_product(product_id=product.product_id)
        raise HttpError(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, message="Unexpected error occurred, please try again later."
        )

    logger.info(f"Created product {product.product_id}")
    return JsonResponse(status=HTTPStatus.CREATED, data={"message": "Product created"})


@api.patch(
    "/update",
    summary="Updates a product",
    description="Updates a product_name or product_description of a product.",
    operation_id="update_record",
    tags=["Products"],
    auth=AuthBearer(),
)
async def _(
        request: HttpRequest,
        product: ProductSchema,
) -> JsonResponse:
    """
    Updates a product.
    :param request:
    :param product:
    :return:
    """
    logger.info(f"Processing API request {request.method} for product {product.product_id}")
    updated = await update_product(product=product)
    if not updated:
        logger.info(f"Product {product.product_id} not found")
        return JsonResponse(status=HTTPStatus.NOT_FOUND, data={"message": "Product not found"})

    logger.info(f"Updated product {product.product_id}")
    return JsonResponse(status=HTTPStatus.OK, data={"message": "Product updated"})


@api.delete(
    "/delete",
    summary="Deletes an existing product",
    description="Deletes an existing product with all offers by its product_id.",
    operation_id="delete_product",
    tags=["Products"],
    auth=AuthBearer(),
)
async def _(
        request: HttpRequest,
        product_id: PositiveInt,
) -> JsonResponse:
    """
    Deletes an existing product.
    :param request:
    :param product_id:
    :return:
    """
    logger.info(f"Processing API request {request.method} for product {product_id}")

    deleted, _ = await delete_product(product_id=product_id)
    if not deleted:
        logger.info(f"Product {product_id} not found for deletion")
        return JsonResponse(status=HTTPStatus.NOT_FOUND, data={"message": "Product not found"})

    logger.info(f"Deleted product {product_id}")
    return JsonResponse(status=HTTPStatus.OK, data={"message": "Product deleted"})


@api.get(
    "/get",
    summary="Get a product",
    description="Get a product by product_id",
    operation_id="get_measurement",
    tags=["Products"],
    auth=AuthBearer(),
)
async def _(
        request: HttpRequest,
        product_id: PositiveInt,
) -> JsonResponse:
    """
    Get a product.
    :param request:
    :param product_id:
    :return:
    """
    logger.info(f"Processing API request {request.method} for product {product_id}")

    obj: Product = await get_product(product_id=product_id)

    if not obj:
        logger.info(f"Product {product_id} not found")
        return JsonResponse(status=HTTPStatus.NOT_FOUND, data={"message": "Product not found"})
    logger.info(f"Retrieved product {product_id}")
    return JsonResponse(status=HTTPStatus.OK, data=ProductSchema(
        product_id=obj.id,
        product_name=obj.name,
        product_description=obj.description
    ).dict())


@api.get(
    "/offers/",
    summary="Get product offers",
    description="Get product offers for a given product",
    operation_id="get_offers",
    tags=["Offers"],
    auth=AuthBearer(),
)
async def _(
        request: HttpRequest,
        product_id: PositiveInt,
) -> JsonResponse:
    logger.info(f"Processing API request {request.method} for product {product_id}")

    offers = await get_offers(product_id=product_id)
    return JsonResponse(status=HTTPStatus.OK, data=offers, safe=False)
