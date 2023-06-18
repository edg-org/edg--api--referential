from typing import List
from api.tools.JWTBearer import JWTBearer, env
from api.salesfinancial.services.SubscriptionTypeService import SubscriptionTypeService
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.salesfinancial.schemas.SubscriptionTypeSchema import (
    SubscriptionTypeInput,
    CreateSubscriptionType,
    SubscriptionTypeUpdate,
    SubscriptionTypeSchema,
    SubscriptionTypePagination
)

router_path = env.api_routers_prefix + env.api_version

subscriptiontypeRouter = APIRouter(
    tags=["Subscription Types"],
    prefix=router_path + "/subscriptiontypes",
    dependencies=[Depends(JWTBearer())]
)

# get all subscription type route
@subscriptiontypeRouter.get(
    "/",
    summary="Getting router for all subscription types",
    description="This router allows to get all subscription types",
    response_model=SubscriptionTypePagination
)
async def list(
    start: int = 0,
    size: int = 100,
    typeService: SubscriptionTypeService = Depends()
):
    count, subscriptiontypes = await typeService.list(start, size)
    return {
        "results": [subscriptiontype for subscriptiontype in subscriptiontypes],
        "total": len(subscriptiontypes),
        "count": count,
        "page_size": size,
        "start_index": start
    }

# get subscription type route
@subscriptiontypeRouter.get(
    "/{code}",
    summary="Getting router a subscription type without items",
    description="This router allows to get a subscription type without items",
    response_model=SubscriptionTypeSchema,
)
async def get(
    code: int,
    typeService: SubscriptionTypeService = Depends(),
):
    subscriptiontype = await typeService.getbycode(code=code)
    if subscriptiontype is None:
        raise HTTPException(
            type_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription Type not found",
        )
    return subscriptiontype

# post subscription type route
@subscriptiontypeRouter.post(
    "/",
    summary="Creation router a subscription type",
    description="This router allows to create a subscription type",
    response_model=List[CreateSubscriptionType]
)
async def create(
    data: List[SubscriptionTypeInput],
    typeService: SubscriptionTypeService = Depends(),
):
    return await typeService.create(data=data)

# update subscription type route
@subscriptiontypeRouter.put(
    "/{code}",
    summary="Update router a subscription type",
    description="This router allows to update a subscription type",
    response_model=SubscriptionTypeSchema
)
async def update(
    code: int,
    data: SubscriptionTypeUpdate,
    typeService: SubscriptionTypeService = Depends(),
    tokendata: dict = Depends(JWTBearer())
):
    return await typeService.update(code=code, tokendata=tokendata, data=data)