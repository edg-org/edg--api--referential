from typing import List
from api.tools.JWTBearer import JWTBearer, env
from api.salesfinancial.services.HousingTypeService import HousingTypeService
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.salesfinancial.schemas.HousingTypeSchema import (
    HousingTypeUpdate,
    CreateHousingType,
    HousingTypeSchema,
    HousingTypePagination
)

router_path = env.api_routers_prefix + env.api_version

housingRouter = APIRouter(
    tags=["Housing Types"],
    prefix=router_path + "/housingtypes",
    dependencies=[Depends(JWTBearer())]
)

# get all housing type route
@housingRouter.get(
    "/",
    summary="Getting router for all housing types",
    description="This router allows to get all housing types",
    response_model=HousingTypePagination,
)
async def list(
    start: int = 0,
    size: int = 100,
    typeService: HousingTypeService = Depends(),
):
    count, housingtypes = await typeService.list(start, size)
    return {
        "results": [housingtype for housingtype in housingtypes],
        "total": len(housingtypes),
        "count": count,
        "page_size": size,
        "start_index": start
    }

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
    response_model=List[CreateHousingType]
)
async def create(
    data: List[CreateHousingType],
    typeService: HousingTypeService = Depends()
):
    return await typeService.create(data=data)

# update housing type route
@housingRouter.put(
    "/{code}",
    summary="Update router a housing type",
    description="This router allows to update a housing type",
    response_model=HousingTypeSchema
)
async def update(
    code: int,
    data: HousingTypeUpdate,
    typeService: HousingTypeService = Depends(),
    tokenpload: dict = Depends(JWTBearer())
):
    return await typeService.update(code=code, tokenpload=tokenpload, data=data)