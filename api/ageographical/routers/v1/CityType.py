from typing import List
from api.tools.JWTBearer import JWTBearer, env
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.ageographical.services.CityTypeService import CityTypeService
from api.ageographical.schemas.CityTypeSchema import (
    CityTypeInput,
    CreateCityType,
    CityTypeUpdate,
    CityTypeSchema
)

router_path = env.api_routers_prefix + env.api_version

citytypeRouter = APIRouter(
    tags=["City Types"],
    prefix=router_path + "/citytypes",
    dependencies=[Depends(JWTBearer())]
)

# get all city types route
@citytypeRouter.get(
    "/",
    summary="Getting router for all city types",
    description="This router allows to get all city types",
    response_model=List[CityTypeSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    typeService: CityTypeService = Depends(),
):
    return await typeService.list(skip, limit)

# get city type route
@citytypeRouter.get(
    "/{code}",
    summary="Getting router a city type without items",
    description="This router allows to get a city type without items",
    response_model=CityTypeSchema,
)
async def get(
    code: int, typeService: CityTypeService = Depends()
):
    citytype = await typeService.getbycode(code=code)
    if citytype is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City Type not found",
        )
    return citytype

# post city type route
@citytypeRouter.post(
    "/",
    summary="Creation router a city type",
    description="This router allows to create a city type",
    response_model=List[CreateCityType]
)
async def create(
    data: List[CityTypeInput],
    typeService: CityTypeService = Depends(),
):
    return await typeService.create(data=data)

# update city type route
@citytypeRouter.put(
    "/{code}",
    summary="Update router a city type",
    description="This router allows to update a city type",
    response_model=CityTypeSchema
)
async def update(
    code: int,
    data: CityTypeUpdate,
    typeService: CityTypeService = Depends(),
    tokendata: dict = Depends(JWTBearer())
):
    return await typeService.update(code=code, tokendata=tokendata, data=data)