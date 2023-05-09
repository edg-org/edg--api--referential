from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.salesfinancial.services.SubscriptionTypeService import (
    SubscriptionTypeService,
)
from api.salesfinancial.schemas.SubscriptionTypeSchema import (
    SubscriptionTypeBase,
    SubscriptionTypeInput,
    CreateSubscriptionType,
    SubscriptionTypeUpdate,
    SubscriptionTypeSchema,
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

subscriptiontypeRouter = APIRouter(
    prefix=router_path + "/subscriptiontypes",
    tags=["Subscription Types"],
)


# get all subscription type route
@subscriptiontypeRouter.get(
    "/",
    summary="Getting router for all subscription types",
    description="This router allows to get all subscription types",
    response_model=List[SubscriptionTypeSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    typeService: SubscriptionTypeService = Depends(),
):
    return await typeService.list(skip, limit)


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
    subscriptiontype = await typeService.getbycode(
        code=code
    )
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
    response_model=List[CreateSubscriptionType],
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
    response_model=SubscriptionTypeSchema,
)
async def update(
    code: int,
    data: SubscriptionTypeUpdate,
    typeService: SubscriptionTypeService = Depends(),
):
    return await typeService.update(code=code, data=data)
