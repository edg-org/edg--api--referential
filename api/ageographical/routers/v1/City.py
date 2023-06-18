from typing import List
from api.tools.JWTBearer import JWTBearer, env
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException
)
from api.ageographical.services.CityService import CityService
from api.ageographical.schemas.CitySchema import (
    CityInput,
    CreateCity,
    CityUpdate,
    CitySchema,
    CityItemSchema,
    CitySearchParams,
    CityPagination
)

router_path = env.api_routers_prefix + env.api_version

cityRouter = APIRouter(
    tags=["Cities"],
    prefix=router_path + "/cities",
    dependencies=[Depends(JWTBearer())]
)

# get all cities route
@cityRouter.get(
    "/",
    summary="Getting router for all cities",
    description="This router allows to get all cities",
    response_model=CityPagination,
)
async def list(
    start: int = 0,
    size: int = 100,
    cityService: CityService = Depends(),
):
    count, cities = await cityService.list(start, size)
    return {
        "results": [city for city in cities],
        "total": len(cities),
        "count": count,
        "page_size": size,
        "start_index": start
    }

# search city by parameters route
@cityRouter.get(
    "/search",
    summary="Getting router a city by parameters without items",
    description="This router allows to get a city by parameters without items",
    response_model=CitySchema,
)
async def search_by_paramas(
    query_params: CitySearchParams = Depends(),
    cityService: CityService = Depends()
):
    city = await cityService.search(query_params=query_params)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    return city

# get city by name route
@cityRouter.get(
    "/{name}",
    summary="Getting router a city by name without items",
    description="This router allows to get a city by name without items",
    response_model=List[CitySchema]
)
async def get_by_name(
    name: str, 
    cityService: CityService = Depends()
):
    city = await cityService.getbyname(name=name)
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
async def get_city_items(
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
    response_model=List[CreateCity]
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
    response_model=CitySchema
)
async def update(
    code: int,
    data: CityUpdate,
    cityService: CityService = Depends(),
    tokendata: dict = Depends(JWTBearer())
):
    return await cityService.update(code=code, tokendata=tokendata, data=data)