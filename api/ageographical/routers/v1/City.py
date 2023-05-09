from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.ageographical.services.CityService import (
    CityService,
)
from api.ageographical.schemas.CitySchema import (
    CityInput,
    CreateCity,
    CityUpdate,
    CitySchema,
    CityItemSchema,
    CitySearchParams
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

cityRouter = APIRouter(
    prefix=router_path + "/cities", tags=["Cities"]
)


# get all cities route
@cityRouter.get(
    "/",
    summary="Getting router for all cities",
    description="This router allows to get all cities",
    response_model=List[CitySchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    cityService: CityService = Depends(),
):
    return await cityService.list(skip, limit)

# get agency route
@cityRouter.get(
    "/{name}",
    summary="Getting router a city without items",
    description="This router allows to get a agency without items",
    response_model=List[CitySchema],
)
async def get(
    name: str, cityService: CityService = Depends()
):
    city = await cityService.getbyname(name=name)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    return city

# get city route
@cityRouter.get(
    "/search",
    summary="Getting router a city without items",
    description="This router allows to get a city without items",
    response_model=CitySchema,
)
async def get(
    params: CitySearchParams = Depends(),
    cityService: CityService = Depends()
):
    city = await cityService.search(params=params)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    return city


# route of get city with item
@cityRouter.get(
    "/items",
    summary="Getting router a city with items",
    description="This router allows to get a city with items",
    response_model=CityItemSchema,
)
async def get_city_item(
    params: CitySearchParams = Depends(),
    cityService: CityService = Depends()
):
    city = await cityService.search(params=params)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    return city


# post city route
@cityRouter.post(
    "/",
    summary="Creation router a city",
    description="This router allows to create a city",
    response_model=List[CreateCity],
)
async def create(
    data: List[CityInput],
    cityService: CityService = Depends(),
):
    return await cityService.create(data=data)


# update city route
@cityRouter.put(
    "/{code}",
    summary="Update router a city",
    description="This router allows to update a city",
    response_model=CitySchema,
)
async def update(
    id: int,
    data: CityUpdate,
    cityService: CityService = Depends(),
):
    return await cityService.update(id=id, data=data)
