from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.electrical.services.MeterDeliveryPointService import MeterDeliveryPointService
from api.electrical.schemas.MeterDeliveryPointSchema import (
    MeterDeliveryPointInput,
    CreateMeterDeliveryPoint,
    MeterDeliveryPointSchema
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

meterdeliveryRouter = APIRouter(
    prefix=router_path + "/meterdeliverypoints",
    tags=["Meter Delivery Points"],
)


# get all meter delivery points route
@meterdeliveryRouter.get(
    "/",
    summary="Getting router for all meter delivery points",
    description="This router allows to get all meter delivery points",
    response_model=List[MeterDeliveryPointSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    meterdeliveryService: MeterDeliveryPointService = Depends(),
):
    return await meterdeliveryService.list(skip, limit)


# get transformer route
@meterdeliveryRouter.get(
    "/{number}",
    summary="Getting router a transformer without items",
    description="This router allows to get a meter delivery point without items",
    response_model=MeterDeliveryPointSchema,
)
async def get(
    id: int,
    meterdeliveryService: MeterDeliveryPointService = Depends(),
):
    supply = await meterdeliveryService.get(id=id)
    if supply is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meter Delivery Point not found",
        )
    return supply


# post transformer route
@meterdeliveryRouter.post(
    "/",
    summary="Creation router a meter delivery point",
    description="This router allows to create a meter delivery point",
    response_model=List[CreateMeterDeliveryPoint],
)
async def create(
    data: List[MeterDeliveryPointInput],
    meterdeliveryService: MeterDeliveryPointService = Depends(),
):
    return await meterdeliveryService.create(data=data)
