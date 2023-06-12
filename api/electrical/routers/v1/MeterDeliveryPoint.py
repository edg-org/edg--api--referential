from typing import List
from api.tools.JWTBearer import JWTBearer, env
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.electrical.services.MeterDeliveryPointService import MeterDeliveryPointService
from api.electrical.schemas.MeterDeliveryPointSchema import (
    MeterDeliveryPointInput,
    CreateMeterDeliveryPoint,
    MeterDeliveryPointSchema,
    MeterDeliveryPointPagination
)

router_path = env.api_routers_prefix + env.api_version

meterdeliveryRouter = APIRouter(
    tags=["Meter Delivery Points"],
    prefix=router_path + "/meterdeliverypoints",
    dependencies=[Depends(JWTBearer())]
)

# get all meter delivery points route
@meterdeliveryRouter.get(
    "/",
    summary="Getting router for all meter delivery points",
    description="This router allows to get all meter delivery points",
    response_model=MeterDeliveryPointPagination,
)
async def list(
    start: int = 0,
    size: int = 100,
    meterdeliveryService: MeterDeliveryPointService = Depends(),
):
    count, meterdeliveries = await meterdeliveryService.list(start, size)
    return {
        "results": [meterdelivery for meterdelivery in meterdeliveries],
        "total": len(meterdeliveries),
        "count": count,
        "page_size": size,
        "start_index": start
    }

# get transformer route
@meterdeliveryRouter.get(
    "/{number}",
    summary="Getting router a transformer without items",
    description="This router allows to get a meter delivery point without items",
    response_model=MeterDeliveryPointSchema
)
async def get(
    id: int,
    meterdeliveryService: MeterDeliveryPointService = Depends()
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
    response_model=List[CreateMeterDeliveryPoint]
)
async def create(
    data: List[MeterDeliveryPointInput],
    meterdeliveryService: MeterDeliveryPointService = Depends()
):
    return await meterdeliveryService.create(data=data)