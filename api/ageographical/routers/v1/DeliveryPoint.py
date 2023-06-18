from typing import List
from api.tools.JWTBearer import JWTBearer, env
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.ageographical.services.DeliveryPointService import DeliveryPointService
from api.ageographical.schemas.DeliveryPointSchema import (
    DeliveryPointInput,
    CreateDeliveryPoint,
    DeliveryPointUpdate,
    DeliveryPointSchema,
    DeliveryPointDetails,
    DeliveryPointPagination
)

router_path = env.api_routers_prefix + env.api_version

deliverypointRouter = APIRouter(
    tags=["Delivery Points"],
    prefix=router_path + "/deliverypoints",
    dependencies=[Depends(JWTBearer())]
)

# get all delivery points route
@deliverypointRouter.get(
    "/",
    summary="Getting router for all delivery points",
    description="This router allows to get all delivery points",
    response_model=DeliveryPointPagination
)
async def list(
    start: int = 0,
    size: int = 100,
    pointService: DeliveryPointService = Depends()
):
    count, points = await pointService.list(start, size)
    return {
        "results": [point for point in points],
        "total": len(points),
        "count": count,
        "page_size": size,
        "start_index": start
    }

# get delivery point route
@deliverypointRouter.get(
    "/{number}",
    summary="Getting router a delivery point without items",
    description="This router allows to get a delivery point without items",
    response_model=DeliveryPointSchema,
)
async def get(
    number: int,
    pointService: DeliveryPointService = Depends()
):
    deliverypoint = await pointService.getbynumber(number=number)
    if deliverypoint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery Point not found",
        )
    return deliverypoint

# get details of delivery point route
@deliverypointRouter.get(
    "/{number}/details",
    summary="Getting router details of delivery point without items",
    description="This router allows to get details of delivery point without items",
    response_model=DeliveryPointDetails,
)
async def getdetails(
    number: int,
    pointService: DeliveryPointService = Depends(),
):
    deliverypoint = await pointService.getdetails(number=number)
    if deliverypoint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery Point not found",
        )
    return deliverypoint

# post delivery point route
@deliverypointRouter.post(
    "/",
    summary="Creation router a delivery point",
    description="This router allows to create a delivery point",
    response_model=List[CreateDeliveryPoint]
)
async def create(
    data: List[DeliveryPointInput],
    pointService: DeliveryPointService = Depends(),
):
    return await pointService.create(data=data)

# update delivery point route
@deliverypointRouter.put(
    "/{number}",
    summary="Update router a delivery point",
    description="This router allows to update a delivery point",
    response_model=DeliveryPointSchema
)
async def update(
    number: int,
    data: DeliveryPointUpdate,
    pointService: DeliveryPointService = Depends(),
    tokendata: dict = Depends(JWTBearer())
):
    return await pointService.update(number=number, tokendata=tokendata, data=data)