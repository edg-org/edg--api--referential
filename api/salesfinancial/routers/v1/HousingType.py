from typing import List
from api.configs.Environment import get_env_var
from api.salesfinancial.services.HousingTypeService import HousingTypeService
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.salesfinancial.schemas.HousingTypeSchema import (
    HousingTypeUpdate,
    CreateHousingType,
    HousingTypeSchema,
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

housingRouter = APIRouter(
    prefix=router_path + "/housingtypes",
    tags=["Housing Types"],
)

# get all housing type route
@housingRouter.get(
    "/",
    summary="Getting router for all housing types",
    description="This router allows to get all housing types",
    response_model=List[HousingTypeSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    typeService: HousingTypeService = Depends(),
):
    return await typeService.list(skip, limit)

# get housing type route
@housingRouter.get(
    "/{code}",
    summary="Getting router a housing type without items",
    description="This router allows to get a housing type without items",
    response_model=HousingTypeSchema,
)
async def get(
    code: int, typeService: HousingTypeService = Depends()
):
    housingtype = await typeService.getbycode(code=code)
    if housingtype is None:
        raise HTTPException(
            type_code=status.HTTP_404_NOT_FOUND,
            detail="Housing Type not found",
        )
    return housingtype

# post housing type route
@housingRouter.post(
    "/",
    summary="Creation router a housing type",
    description="This router allows to create a housing type",
    response_model=List[CreateHousingType],
)
async def create(
    data: List[CreateHousingType],
    typeService: HousingTypeService = Depends(),
):
    return await typeService.create(data=data)

# update housing type route
@housingRouter.put(
    "/{code}",
    summary="Update router a housing type",
    description="This router allows to update a housing type",
    response_model=HousingTypeSchema,
)
async def update(
    code: int,
    data: HousingTypeUpdate,
    typeService: HousingTypeService = Depends(),
):
    return await typeService.update(code=code, data=data)