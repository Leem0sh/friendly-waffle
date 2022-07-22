# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from typing import Final

api: Final = NinjaAPI(title="Dimensions JSON API", version="0.3.0", urls_namespace="dimensions-api")


@api.post(
    "/measurement",
    summary="Create a new Measurement",
    description=(
        f"Creates a new Measurement of a Variant. The status code {HTTPStatus.CONFLICT!r} "
        "is returned if the request already exists."
    ),
    operation_id="create_measurement",
    response={
        HTTPStatus.CREATED: MeasurementCreated,
        HTTPStatus.CONFLICT: TypedDict("Conflict", {"detail": str}),
    },
    tags=["dimensions"],
    auth=AuthBearer(),
)
async def _(

) -> None:
    pass

@api.get(
    "/measurement/{project_id}/{model}/{content_checksum}",
    summary="Read existing Measurement",
    description="Read existing Measurement of a Variant.",
    operation_id="read_measurement",
    response=Measurement,
    tags=["dimensions"],
    auth=AuthBearer(),
)
async def _(
    request: HttpRequest,
    project_id: int,
    model: DimensionsModelTextChoices,
    content_checksum: ContentChecksum,
) -> None:

    pass


