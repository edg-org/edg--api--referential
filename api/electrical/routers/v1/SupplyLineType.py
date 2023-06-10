from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.electrical.services.SupplyLineTypeService import SupplyLineTypeService
from api.electrical.schemas.SupplyLineTypeSchema import (
    SupplyLineTypeInput,
    CreateSupplyLineType,
    SupplyLineTypeUpdate,
    SupplyLineTypeSchema
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

linetypeRouter = APIRouter(
    prefix=router_path + "/supplylinetypes", tags=["Supply Line Types"]
)


# get all supplyline types route
@linetypeRouter.get(
    "/",
    summary="Getting router for all supply line types",
    description="This router allows to get all supply line types",
    response_model=List[SupplyLineTypeSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    supplylineService: SupplyLineTypeService = Depends(),
):
    return await supplylineService.list(skip, limit)


# get supplyline type route
@linetypeRouter.get(
    "/{code}",
    summary="Getting router a supply line type without items",
    description="This router allows to get a supply line type without items",
    response_model=SupplyLineTypeSchema,
)
async def get(
    code: int, supplylineService: SupplyLineTypeService = Depends()
):
    supplyline = await supplylineService.getbycode(code=code)
    if supplylinetype is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supply Line Type not found",
        )
    return supplyline


# post supplyline type route
@linetypeRouter.post(
    "/",
    summary="Creation router a supply line type",
    description="This router allows to create a supply line type",
    response_model=List[CreateSupplyLineType],
)
async def create(
    data: List[SupplyLineTypeInput],
    supplylineService: SupplyLineTypeService = Depends(),
):
    return await supplylineService.create(data=data)


# update supplyline type route
@linetypeRouter.put(
    "/{code}",
    summary="Update router a supply line type",
    description="This router allows to update a supply line type",
    response_model=SupplyLineTypeSchema,
)
async def update(
    code: int,
    data: SupplyLineTypeUpdate,
    supplylineService: SupplyLineTypeService = Depends(),
):
    return await supplylineService.update(code=code, data=data)