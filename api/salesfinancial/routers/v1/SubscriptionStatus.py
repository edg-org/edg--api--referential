from typing import List
from api.tools.JWTBearer import JWTBearer, env
from api.salesfinancial.services.SubscriptionStatusService import SubscriptionStatusService
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.salesfinancial.schemas.SubscriptionStatusSchema import (
    CreateSubscriptionStatus,
    SubscriptionStatusUpdate,
    SubscriptionStatusSchema,
)

router_path = env.api_routers_prefix + env.api_version

subscriptionstatusRouter = APIRouter(
    tags=["Subscription Status"],
    prefix=router_path + "/subscriptionstatus",
    dependencies=[Depends(JWTBearer())]
)

# get all subscription status route
@subscriptionstatusRouter.get(
    "/",
    summary="Getting router for all subscription status",
    description="This router allows to get all subscription status",
    response_model=List[SubscriptionStatusSchema],
)
async def list(
    start: int = 0,
    size: int = 100,
    statusService: SubscriptionStatusService = Depends(),
):
    return await statusService.list(start, size)

# get subscription status route
@subscriptionstatusRouter.get(
    "/{code}",
    summary="Getting router a subscription status without items",
    description="This router allows to get a subscription status without items",
    response_model=SubscriptionStatusSchema,
)
async def get(
    code: int,
    statusService: SubscriptionStatusService = Depends(),
):
    subscriptionstatus = await statusService.getbycode(code=code)
    if subscriptionstatus is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription Status not found",
        )
    return subscriptionstatus

# post subscription status route
@subscriptionstatusRouter.post(
    "/",
    summary="Creation router a subscription status",
    description="This router allows to create a subscription status",
    response_model=List[CreateSubscriptionStatus]
)
async def create(
    data: List[CreateSubscriptionStatus],
    statusService: SubscriptionStatusService = Depends(),
):
    return await statusService.create(data=data)

# update subscription status route
@subscriptionstatusRouter.put(
    "/{code}",
    summary="Update router a subscription status",
    description="This router allows to update a subscription status",
    response_model=SubscriptionStatusSchema
)
async def update(
    code: int,
    data: SubscriptionStatusUpdate,
    statusService: SubscriptionStatusService = Depends(),
    tokendata: dict = Depends(JWTBearer())
):
    return await statusService.update(code=code, tokendata=tokendata, data=data)