from typing import List
from api.configs.Environment import get_env_var
from fastapi import Depends, APIRouter, status, HTTPException
from api.sales_financial.services.SubscriptionLevelService import SubscriptionLevelService
from api.sales_financial.schemas.SubscriptionLevelSchema import (
    SubscriptionLevelBase, 
    CreateSubscriptionLevel,
    SubscriptionLevelSchema
)

env = get_env_var()
router_path = env.api_routers_prefix+env.api_version

subscriptionlevelRouter = APIRouter(
    prefix=router_path+"/subscriptionfrequencies",
    tags=["Subscription Levels"]
)

#get all subscription level route
@subscriptionlevelRouter.get(
    "/",
    summary="Getting router for all subscription levels",
    description="This router allows to get all subscription levels",
    response_model=List[SubscriptionLevelSchema]
)
async def list(skip: int=0, limit: int=100, levelService: SubscriptionLevelService = Depends()):
    return await levelService.list(skip, limit)

#get subscription level route
@subscriptionlevelRouter.get(
    "/{code}",
    summary="Getting router a subscription level without items",
    description="This router allows to get a subscription level without items",
    response_model=SubscriptionLevelSchema
)
async def get(code: int, levelService: SubscriptionLevelService = Depends()):
    subscriptionlevel = await levelService.getbycode(code=code)
    if subscriptionlevel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription Level not found")
    return subscriptionlevel

#post subscription level route
@subscriptionlevelRouter.post(
    "/",
    summary="Creation router a subscription level",
    description="This router allows to create a subscription level",
    response_model=List[CreateSubscriptionLevel]
)
async def create(data: List[CreateSubscriptionLevel], levelService: SubscriptionLevelService = Depends()):
    return await levelService.create(data=data)

#update subscription level route
@subscriptionlevelRouter.put(
    "/{code}",
    summary="Update router a subscription level",
    description="This router allows to update a subscription level",
    response_model=SubscriptionLevelSchema
)
async def update(code: int, data: SubscriptionLevelBase, levelService: SubscriptionLevelService = Depends()):
    return await levelService.update(code=code, data=data)