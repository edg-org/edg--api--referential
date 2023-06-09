from typing import List
from api.tools.JWTBearer import JWTBearer, env
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.ageographical.services.CityLevelService import CityLevelService
from api.ageographical.schemas.CityLevelSchema import (
    CityLevelInput,
    CreateCityLevel,
    CityLevelUpdate,
    CityLevelSchema,
)


router_path = env.api_routers_prefix + env.api_version

citylevelRouter = APIRouter(
    tags=["City Levels"],
    prefix=router_path + "/citylevels",
    dependencies=[Depends(JWTBearer())]
)

# get all city levels route
@citylevelRouter.get(
    "/",
    summary="Getting router for all city levels",
    description="This router allows to get all city levels",
    response_model=List[CityLevelSchema],
)
async def list(
    start: int = 0,
    size: int = 100,
    levelService: CityLevelService = Depends(),
):
    return await levelService.list(start, size)

# get city level route
@citylevelRouter.get(
    "/{code}",
    summary="Getting router a city level without items",
    description="This router allows to get a city level without items",
    response_model=CityLevelSchema,
)
async def get(
    code: int, levelService: CityLevelService = Depends()
):
    citylevel = await levelService.getbycode(code=code)
    if citylevel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City Level not found",
        )
    return citylevel

# post city level route
@citylevelRouter.post(
    "/",
    summary="Creation router a city level",
    description="This router allows to create a city level",
    response_model=List[CreateCityLevel]
)
async def create(
    data: List[CityLevelInput],
    levelService: CityLevelService = Depends()
):
    return await levelService.create(data=data)

# update city level route
@citylevelRouter.put(
    "/{code}",
    summary="Update router a city level",
    description="This router allows to update a city level",
    response_model=CityLevelSchema
)
async def update(
    code: int,
    data: CityLevelUpdate,
    levelService: CityLevelService = Depends(),
    tokendata: dict = Depends(JWTBearer())
):
    return await levelService.update(code=code, tokendata= tokendata, data=data)