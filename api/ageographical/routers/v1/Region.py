from typing import List
from api.tools.JWTBearer import JWTBearer, env
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.ageographical.services.RegionService import RegionService
from api.ageographical.schemas.RegionSchema import (
    RegionInput,
    RegionSchema,
    RegionUpdate,
    CreateRegion,
    RegionItemSchema
)

router_path = env.api_routers_prefix + env.api_version

regionRouter = APIRouter(
    prefix=router_path + "/regions",
    tags=["Administrative Regions"],
    dependencies=[Depends(JWTBearer())]
)

# get all administrative regions route
@regionRouter.get(
    "/",
    summary="Getting router for all administrative regions",
    description="This router allows to get all administrative regions",
    response_model=list[RegionSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    regionService: RegionService = Depends(),
):
    return await regionService.list(skip, limit)

# get administrative region route
@regionRouter.get(
    "/{code}",
    summary="Getting router a administrative region without items",
    description="This router allows to get a administrative region without items",
    response_model=RegionSchema,
)
async def get(
    code: int, 
    regionService: RegionService = Depends()
):
    region = await regionService.getbycode(code=code)
    if region is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Administrative Region not found",
        )
    return region

# route of get administrative region with item
@regionRouter.get(
    "/{code}/items",
    summary="Getting router a administrative region with items",
    description="This router allows to get a administrative region with items",
    response_model=RegionItemSchema,
)
async def get_region_items(
    code: int,
    regionService: RegionService = Depends()
):
    region = await regionService.getbycode(code=code)
    if region is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Administrative Region not found",
        )
    return region

# post administrative region route
@regionRouter.post(
    "/",
    summary="Creation router a administrative region",
    description="This router allows to create a administrative region",
    response_model=List[CreateRegion]
)
async def create(
    data: List[RegionInput],
    regionService: RegionService = Depends(),
):
    return await regionService.create(data=data)

# update administrative region route
@regionRouter.put(
    "/{code}",
    summary="Update router a administrative region",
    description="This router allows to update a administrative region",
    response_model=RegionSchema
)
async def update(
    code: int,
    data: RegionUpdate,
    regionService: RegionService = Depends(),
    tokendata: dict = Depends(JWTBearer())
):
    return await regionService.update(code=code, tokendata=tokendata, data=data)