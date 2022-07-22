# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from http import HTTPStatus
from typing import Final

from django.http import HttpRequest, JsonResponse
from ninja import NinjaAPI
from ninja.errors import HttpError

from app.api_auth import AuthBearer
from app.db.operations import create_product, delete_product, get_product, update_product
from app.models import Product
from app.schemas import ProductSchema

logger: Final = logging.getLogger(__name__)
api: Final = NinjaAPI(title="Applift JSON API", version="0.1.0", urls_namespace="applift-api")


# TODO
@api.post(
    "/create-product",
    summary="Creates a new product",
    #     description=(
    #             f"Creates a new Measurement of a Variant. The status code {HTTPStatus.CONFLICT!r} "
    #             "is returned if the request already exists."
    #     ),
    operation_id="create_product",
    tags=["database"],
    auth=AuthBearer(),
)
async def _(
        request: HttpRequest,
        product: ProductSchema,
) -> JsonResponse:  # | HttpError?
    """
    Creates a new product.
    :param request:
    :param product:
    :return:
    """
    logger.info(f"Processing API re,.quest {request.method}")
    created = await create_product(product=product)
    if not created:
        logger.info(f"Product {product.product_id} already exists")
        raise HttpError(
            status_code=HTTPStatus.CONFLICT, message="This record already exists."
        )

    logger.info(f"Created product {product.product_id}")
    return JsonResponse(status=HTTPStatus.CREATED, data={"message": "Product created"})


@api.patch(
    "/update",
    summary="Updates a product",
    #     description=(
    #             f"Creates a new Measurement of a Variant. The status code {HTTPStatus.CONFLICT!r} "
    #             "is returned if the request already exists."
    #     ),
    operation_id="update_record",
    tags=["database"],
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
    logger.info(f"Processing API request {request.method}")
    updated = await update_product(product=product)
    if not updated:
        logger.info(f"Product {product.product_id} not found")
        return JsonResponse(status=HTTPStatus.NOT_FOUND, data={"message": "Product not found"})

    logger.info(f"Updated product {product.product_id}")
    return JsonResponse(status=HTTPStatus.OK, data={"message": "Product updated"})


@api.delete(
    "/delete",
    summary="Deletes an existing product",
    #     description=()
    operation_id="delete_product",

    tags=["database"],
    auth=AuthBearer(),
)
async def _(
        request: HttpRequest,
        product_id: str,
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
    #     description=(
    #             f"Creates a new Measurement of a Variant. The status code {HTTPStatus.CONFLICT!r} "
    #             "is returned if the request already exists."
    #     ),
    operation_id="get_measurement",
    tags=["database"],
    auth=AuthBearer(),
)
async def _(
        request: HttpRequest,
        product_id: str,
) -> JsonResponse:
    """
    Get a product.
    :param request:
    :param product_id:
    :return:
    """
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

# @api.get(
#     "/measurement/",
#     # summary="Read existing Measurement",
#     # description="Read existing Measurement of a Variant.",
#     # operation_id="read_measurement",
#     # response=Measurement,
#     tags=["default"],
#     auth=AuthBearer(),
# )
# async def _(
#
# ) -> None:
#     pass
