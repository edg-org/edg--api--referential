from typing import List
from api.tools.JWTBearer import JWTBearer, env
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.ageographical.services.NaturalZoneService import ZoneService
from api.ageographical.schemas.NaturalZoneSchema import (
    ZoneInput,
    ZoneSchema,
    ZoneUpdate,
    CreateZone,
    ZoneItemSchema,
)

router_path = env.api_routers_prefix + env.api_version

zoneRouter = APIRouter(
    tags=["Natural Regions"],
    prefix=router_path + "/naturalregions"
)

# post natural region route
@zoneRouter.post(
    "/",
    summary="Creation router a natural region",
    description="This router allows to create a natural region",
    response_model=List[CreateZone],
    dependencies=[Depends(JWTBearer())]
)
async def create(
    data: List[ZoneInput],
    zoneService: ZoneService = Depends()
):
    return await zoneService.create(data=data)

# get all natural regions route
@zoneRouter.get(
    "/",
    summary="Getting router for all natural regions",
    description="This router allows to get all natural regions",
    response_model=List[ZoneSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    zoneService: ZoneService = Depends(),
):
    return await zoneService.list(skip, limit)

# get natural region route
@zoneRouter.get(
    "/{code}",
    summary="Getting router a natural region by code without items",
    description="This router allows to get a natural region by code without items",
    response_model=ZoneSchema,
)
async def get_by_code(
    code: int, 
    zoneService: ZoneService = Depends()
):
    zone = await zoneService.getbycode(code=code)
    if zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Natural Zone not found",
        )
    return zone

# route of get natural region with item
@zoneRouter.get(
    "/{code}/items",
    summary="Getting router a natural region with items",
    description="This router allows to get a natural region with items",
    response_model=ZoneItemSchema,
)
async def get_zone_item(
    code: int, 
    zoneService: ZoneService = Depends()
):
    zone = await zoneService.getbycode(code=code)
    if zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Natural Zone not found",
        )
    return zone

# update natural region route
@zoneRouter.put(
    "/{code}",
    summary="Update router a natural region",
    description="This router allows to update a natural region",
    response_model=ZoneSchema,
    dependencies=[Depends(JWTBearer())]
)
async def update(
    code: int,
    data: ZoneUpdate,
    zoneService: ZoneService = Depends(),
):
    return await zoneService.update(code=code, data=data)