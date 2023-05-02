from typing import List
from api.configs.Environment import get_env_var
from fastapi import Depends, APIRouter, status, HTTPException
from api.sales_financial.services.SubscriptionStatusService import SubscriptionStatusService
from api.sales_financial.schemas.SubscriptionStatusSchema import (
    SubscriptionStatusBase, 
    CreateSubscriptionStatus,
    SubscriptionStatusSchema
)

env = get_env_var()
router_path = env.api_routers_prefix+env.api_version

subscriptionstatusRouter = APIRouter(
    prefix=router_path+"/subscriptionstatus",
    tags=["Subscription Status"]
)

#get all subscription status route
@subscriptionstatusRouter.get(
    "/",
    summary="Getting router for all subscription status",
    description="This router allows to get all subscription status",
    response_model=List[SubscriptionStatusSchema]
)
async def list(skip: int=0, limit: int=100, statusService: SubscriptionStatusService = Depends()):
    return await statusService.list(skip, limit)

#get subscription status route
@subscriptionstatusRouter.get(
    "/{code}",
    summary="Getting router a subscription status without items",
    description="This router allows to get a subscription status without items",
    response_model=SubscriptionStatusSchema
)
async def get(code: int, statusService: SubscriptionStatusService = Depends()):
    subscriptionstatus = await statusService.getbycode(code=code)
    if subscriptionstatus is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription Status not found")
    return subscriptionstatus

#post subscription status route
@subscriptionstatusRouter.post(
    "/",
    summary="Creation router a subscription status",
    description="This router allows to create a subscription status",
    response_model=List[CreateSubscriptionStatus]
)
async def create(data: List[CreateSubscriptionStatus], statusService: SubscriptionStatusService = Depends()):
    return await statusService.create(data=data)

#update subscription status route
@subscriptionstatusRouter.put(
    "/{code}",
    summary="Update router a subscription status",
    description="This router allows to update a subscription status",
    response_model=SubscriptionStatusSchema
)
async def update(code: int, data: SubscriptionStatusBase, statusService: SubscriptionStatusService = Depends()):
    return await statusService.update(code=code, data=data)