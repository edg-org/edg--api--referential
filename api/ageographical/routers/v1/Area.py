from typing import List
from api.tools.JWTBearer import JWTBearer, env
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.ageographical.services.AreaService import AreaService
from api.ageographical.schemas.AreaSchema import (
    AreaInput,
    CreateArea,
    AreaSchema,
    AreaUpdate,
    AreaItemSchema,
)

router_path = env.api_routers_prefix + env.api_version

areaRouter = APIRouter(
    tags=["Areas"],
    prefix=router_path + "/areas"
)

# get all areas route
@areaRouter.get(
    "/",
    summary="Getting router for all areas",
    description="This router allows to get all areas",
    response_model=List[AreaSchema]
)
async def list(
    skip: int = 0, 
    limit: int = 100,
    areaService: AreaService = Depends()
):
    return await areaService.list(skip, limit)

# get area route
@areaRouter.get(
    "/{code}",
    summary="Getting router a area without items",
    description="This router allows to get a area without items",
    response_model=AreaSchema,
)
async def get(
    code: int, 
    areaService: AreaService = Depends()
):
    area = await areaService.getbycode(code=code)
    if area is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Area not found",
        )
    return area

# route of get area with item
@areaRouter.get(
    "/{code}/items",
    summary="Getting router a area with items",
    description="This router allows to get a area with items",
    response_model=AreaItemSchema,
)
async def get_area_item(
    code: int, areaService: AreaService = Depends()
):
    area = await areaService.getbycode(code=code)
    if area is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Area not found",
        )
    return area

# post area route
@areaRouter.post(
    "/",
    summary="Creation router a area",
    description="This router allows to create a area",
    response_model=List[CreateArea],
    dependencies=[Depends(JWTBearer())]
)
async def create(
    data: List[AreaInput],
    areaService: AreaService = Depends(),
):
    return await areaService.create(data=data)

# update area route
@areaRouter.put(
    "/{code}",
    summary="Update router a area",
    description="This router allows to update a area",
    response_model=AreaSchema,
    dependencies=[Depends(JWTBearer())]
)
async def update(
    code: int,
    data: AreaUpdate,
    areaService: AreaService = Depends(),
):
    return await areaService.update(code=code, data=data)