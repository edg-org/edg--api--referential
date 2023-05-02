from typing import List
from api.configs.Environment import get_env_var
from fastapi import Depends, APIRouter, status, HTTPException
from api.geographical.services.NaturalZoneService import ZoneService
from api.geographical.schemas.NaturalZoneSchema import (
    ZoneBase,
    ZoneSchema, 
    CreateZone,
    ZoneItemSchema
)

env = get_env_var()
router_path = env.api_routers_prefix+env.api_version

zoneRouter = APIRouter(
    prefix=router_path+"/naturalzones",
    tags=["Natural Regions"]
)

#get all natural regions route
@zoneRouter.get(
    "/",
    summary="Getting router for all natural regions",
    description="This router allows to get all natural regions",
    response_model=List[ZoneSchema]
)
async def list(skip: int=0, limit: int=100, zoneService: ZoneService = Depends()):
    return await zoneService.list(skip, limit)

#get natural region route
@zoneRouter.get(
    "/{code}",
    summary="Getting router a natural region by code without items",
    description="This router allows to get a natural region by code without items",
    response_model=ZoneSchema
)
async def get_by_code(code: int, zoneService: ZoneService = Depends()):
    zone = await zoneService.getbycode(code=code)
    if zone is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Natural Zone not found")
    return zone

# route of get natural region with item
@zoneRouter.get(
    "/items/{code}",
    summary="Getting router a natural region with items",
    description="This router allows to get a natural region with items",
    response_model=ZoneItemSchema
)
async def get_zone_item(code: int, zoneService: ZoneService = Depends()):
    zone = await zoneService.getbycode(code=code)
    if zone is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Natural Zone not found")
    return zone

#post natural region route
@zoneRouter.post(
    "/",
    summary="Creation router a natural region",
    description="This router allows to create a natural region",
    response_model=List[CreateZone]
)
async def create(data: List[CreateZone], zoneService: ZoneService = Depends()):
    return await zoneService.create(data=data)

#update natural region route
@zoneRouter.put(
    "/{code}",
    summary="Update router a natural region",
    description="This router allows to update a natural region",
    response_model=ZoneSchema
)
async def update(code: int, data: ZoneBase, zoneService: ZoneService = Depends()):
    return await zoneService.update(id=code, data=data)