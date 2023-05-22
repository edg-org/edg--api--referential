from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.salesfinancial.services.TrackingTypeService import TrackingTypeService
from api.salesfinancial.schemas.TrackingTypeSchema import (
    TrackingTypeBase,
    CreateTrackingType,
    TrackingTypeUpdate,
    TrackingTypeSchema,
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

trackingRouter = APIRouter(
    prefix=router_path + "/trackingtypes",
    tags=["Tracking Types"],
)


# get all tracking type route
@trackingRouter.get(
    "/",
    summary="Getting router for all tracking types",
    description="This router allows to get all tracking types",
    response_model=List[TrackingTypeSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    typeService: TrackingTypeService = Depends(),
):
    return await typeService.list(skip, limit)


# get tracking type route
@trackingRouter.get(
    "/{code}",
    summary="Getting router a tracking type without items",
    description="This router allows to get a tracking type without items",
    response_model=TrackingTypeSchema,
)
async def get(
    code: int, typeService: TrackingTypeService = Depends()
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
    response_model=List[CreateTrackingType],
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
    response_model=TrackingTypeSchema,
)
async def update(
    code: int,
    data: TrackingTypeUpdate,
    typeService: TrackingTypeService = Depends(),
):
    return await typeService.update(code=code, data=data)
