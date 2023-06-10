from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.ageographical.services.DeliveryPointService import DeliveryPointService
from api.ageographical.schemas.DeliveryPointSchema import (
    DeliveryPointInput,
    CreateDeliveryPoint,
    DeliveryPointUpdate,
    DeliveryPointSchema,
    DeliveryPointDetails
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

deliverypointRouter = APIRouter(
    prefix=router_path + "/deliverypoints",
    tags=["Delivery Points"]
)

# get all delivery points route
@deliverypointRouter.get(
    "/",
    summary="Getting router for all delivery points",
    description="This router allows to get all delivery points",
    response_model=List[DeliveryPointSchema]
)
async def list(
    skip: int = 0,
    limit: int = 100,
    deliverypointService: DeliveryPointService = Depends()
):
    return await deliverypointService.list(skip, limit)

# get delivery point route
@deliverypointRouter.get(
    "/{number}",
    summary="Getting router a delivery point without items",
    description="This router allows to get a delivery point without items",
    response_model=DeliveryPointSchema,
)
async def get(
    number: int,
    deliverypointService: DeliveryPointService = Depends(),
):
    deliverypoint = await deliverypointService.getbynumber(number=number)
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
    deliverypointService: DeliveryPointService = Depends(),
):
    deliverypoint = await deliverypointService.getdetails(number=number)
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
    response_model=List[CreateDeliveryPoint],
)
async def create(
    data: List[DeliveryPointInput],
    deliverypointService: DeliveryPointService = Depends(),
):
    return await deliverypointService.create(data=data)

# update delivery point route
@deliverypointRouter.put(
    "/{number}",
    summary="Update router a delivery point",
    description="This router allows to update a delivery point",
    response_model=DeliveryPointSchema,
)
async def update(
    number: int,
    data: DeliveryPointUpdate,
    deliverypointService: DeliveryPointService = Depends(),
):
    return await deliverypointService.update(
        number=number, 
        data=data
    )