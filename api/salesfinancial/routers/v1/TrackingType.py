from typing import List
from api.tools.JWTBearer import JWTBearer, env
from api.salesfinancial.services.TrackingTypeService import TrackingTypeService
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.salesfinancial.schemas.TrackingTypeSchema import (
    CreateTrackingType,
    TrackingTypeUpdate,
    TrackingTypeSchema
)

router_path = env.api_routers_prefix + env.api_version

trackingRouter = APIRouter(
    tags=["Tracking Types"],
    prefix=router_path + "/trackingtypes",
    dependencies=[Depends(JWTBearer())]
)

# get all tracking type route
@trackingRouter.get(
    "/",
    summary="Getting router for all tracking types",
    description="This router allows to get all tracking types",
    response_model=List[TrackingTypeSchema]
)
async def list(
    start: int = 0,
    size: int = 100,
    typeService: TrackingTypeService = Depends(),
):
    return await typeService.list(start, size)

# get tracking type route
@trackingRouter.get(
    "/{code}",
    summary="Getting router a tracking type without items",
    description="This router allows to get a tracking type without items",
    response_model=TrackingTypeSchema,
)
async def get(
    code: int, 
    typeService: TrackingTypeService = Depends()
):
    trackingtype = await typeService.getbycode(code=code)
    if trackingtype is None:
        raise HTTPException(
            type_code=status.HTTP_404_NOT_FOUND,
            detail="Tracking Type not found",
        )
    return trackingtype

# post tracking type route
@trackingRouter.post(
    "/",
    summary="Creation router a tracking type",
    description="This router allows to create a tracking type",
    response_model=List[CreateTrackingType]
)
async def create(
    data: List[CreateTrackingType],
    typeService: TrackingTypeService = Depends(),
):
    return await typeService.create(data=data)

# update tracking type route
@trackingRouter.put(
    "/{code}",
    summary="Update router a tracking type",
    description="This router allows to update a tracking type",
    response_model=TrackingTypeSchema
)
async def update(
    code: int,
    data: TrackingTypeUpdate,
    typeService: TrackingTypeService = Depends(),
    tokendata: dict = Depends(JWTBearer())
):
    return await typeService.update(code=code, tokendata=tokendata, data=data)