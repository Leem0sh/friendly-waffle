# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from typing import Final

from ninja import NinjaAPI

from app.api_auth import AuthBearer
from app.schemas import Product

api: Final = NinjaAPI(title="Applift JSON API", version="0.1.0", urls_namespace="applift-api")


# TODO
@api.post(
    "/create",
    #     summary="Create a new Measurement",
    #     description=(
    #             f"Creates a new Measurement of a Variant. The status code {HTTPStatus.CONFLICT!r} "
    #             "is returned if the request already exists."
    #     ),
    #     operation_id="create_record",
    #     response={
    #         HTTPStatus.CREATED: MeasurementCreated,
    #         HTTPStatus.CONFLICT: TypedDict("Conflict", {"detail": str}),
    #     },
    tags=["database"],
    auth=AuthBearer(),
)
async def _(
        product: Product
) -> None:
    pass


@api.put(
    "/update",
    #     summary="Create a new Measurement",
    #     description=(
    #             f"Creates a new Measurement of a Variant. The status code {HTTPStatus.CONFLICT!r} "
    #             "is returned if the request already exists."
    #     ),
    #     operation_id="update_record",
    #     response={
    #         HTTPStatus.CREATED: MeasurementCreated,
    #         HTTPStatus.CONFLICT: TypedDict("Conflict", {"detail": str}),
    #     },
    tags=["database"],
    auth=AuthBearer(),
)
async def _(

) -> None:
    pass


@api.delete(
    "/delete",
    #     summary="Create a new Measurement",
    #     description=(
    #             f"Creates a new Measurement of a Variant. The status code {HTTPStatus.CONFLICT!r} "
    #             "is returned if the request already exists."
    #     ),
    #     operation_id="create_measurement",
    #     response={
    #         HTTPStatus.CREATED: MeasurementCreated,
    #         HTTPStatus.CONFLICT: TypedDict("Conflict", {"detail": str}),
    #     },
    tags=["database"],
    auth=AuthBearer(),
)
async def _(

) -> None:
    pass


@api.get(
    "/get",
    #     summary="Create a new Measurement",
    #     description=(
    #             f"Creates a new Measurement of a Variant. The status code {HTTPStatus.CONFLICT!r} "
    #             "is returned if the request already exists."
    #     ),
    #     operation_id="create_measurement",
    #     response={
    #         HTTPStatus.CREATED: MeasurementCreated,
    #         HTTPStatus.CONFLICT: TypedDict("Conflict", {"detail": str}),
    #     },
    tags=["database"],
    auth=AuthBearer(),
)
async def _(

) -> None:
    pass


@api.get(
    "/measurement/{project_id}/{model}/{content_checksum}",
    # summary="Read existing Measurement",
    # description="Read existing Measurement of a Variant.",
    # operation_id="read_measurement",
    # response=Measurement,
    tags=["default"],
    auth=AuthBearer(),
)
async def _(

) -> None:
    pass
