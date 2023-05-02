from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.electrical.services.DeliveryPointService import (
    DeliveryPointService,
)
from api.electrical.schemas.DeliveryPointSchema import (
    DeliveryPointBase,
    CreateDeliveryPoint,
    DeliveryPointSchema,
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

deliveryRouter = APIRouter(
    prefix=router_path + "/deliverypoints",
    tags=["Delivery Points"],
)


# get all delivery points route
@deliveryRouter.get(
    "/",
    summary="Getting router for all delivery points",
    description="This router allows to get all delivery points",
    response_model=List[DeliveryPointSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    deliveryService: DeliveryPointService = Depends(),
):
    return await deliveryService.list(skip, limit)


# get transformer route
@deliveryRouter.get(
    "/{number}",
    summary="Getting router a transformer without items",
    description="This router allows to get a delivery point without items",
    response_model=DeliveryPointSchema,
)
async def get(
    number: int,
    deliveryService: DeliveryPointService = Depends(),
):
    departure = await deliveryService.getbynumber(
        number=number
    )
    if departure is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery Point not found",
        )
    return departure


# post transformer route
@deliveryRouter.post(
    "/",
    summary="Creation router a delivery point",
    description="This router allows to create a delivery point",
    response_model=List[CreateDeliveryPoint],
)
async def create(
    data: List[CreateDeliveryPoint],
    deliveryService: DeliveryPointService = Depends(),
):
    return await deliveryService.create(data=data)


# update transformer route
@deliveryRouter.put(
    "/{number}",
    summary="Update router a delivery point",
    description="This router allows to update a delivery point",
    response_model=DeliveryPointSchema,
)
async def update(
    number: int,
    data: DeliveryPointBase,
    deliveryService: DeliveryPointService = Depends(),
):
    return await deliveryService.update(
        number=number, data=data
    )
