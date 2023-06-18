from typing import List
from api.tools.JWTBearer import JWTBearer, env
from api.salesfinancial.services.PricingHistoryService import PricingHistoryService
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException
)
from api.salesfinancial.schemas.PricingHistorySchema import (
    CreatePricingHistory,
    PricingHistorySchema,
    PrincingHistoryPagination
)

router_path = env.api_routers_prefix + env.api_version

pricinghistoryRouter = APIRouter(
    tags=["Pricing Histories"],
    prefix=router_path + "/pricinghistories",
    dependencies=[Depends(JWTBearer())]
)

# get all pricing history route
@pricinghistoryRouter.get(
    "/",
    summary="Getting router for all pricing historys",
    description="This router allows to get all pricing historys",
    response_model=PrincingHistoryPagination
)
async def list(
    start: int = 0,
    size: int = 100,
    historyService: PricingHistoryService = Depends(),
):
    count, histories = await historyService.list(start, size)
    return {
        "results": [history for history in histories],
        "total": len(histories),
        "count": count,
        "page_size": size,
        "start_index": start
    }

# get pricing history route
@pricinghistoryRouter.get(
    "/{code}",
    summary="Getting router a pricing history without items",
    description="This router allows to get a pricing history without items",
    response_model=PricingHistorySchema
)
async def get(
    code: int,
    historyService: PricingHistoryService = Depends(),
):
    pricinghistory = await historyService.getbycode(code=code)
    if pricinghistory is None:
        raise HTTPException(
            history_code=status.HTTP_404_NOT_FOUND,
            detail="Pricing History not found",
        )
    return pricinghistory

# post pricing history route
@pricinghistoryRouter.post(
    "/",
    summary="Creation router a pricing history",
    description="This router allows to create a pricing history",
    response_model=List[CreatePricingHistory],
)
async def create(
    data: List[CreatePricingHistory],
    historyService: PricingHistoryService = Depends()
):
    return await historyService.create(data=data)