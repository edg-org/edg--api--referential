from typing import List
from api.tools.JWTBearer import JWTBearer, env
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.electrical.services.SupplyLineTypeService import SupplyLineTypeService
from api.electrical.schemas.SupplyLineTypeSchema import (
    SupplyLineTypeInput,
    CreateSupplyLineType,
    SupplyLineTypeUpdate,
    SupplyLineTypeSchema
)

router_path = env.api_routers_prefix + env.api_version

linetypeRouter = APIRouter(
    tags=["Supply Line Types"],
    prefix=router_path + "/supplylinetypes"
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
    supplylinetypeService: SupplyLineTypeService = Depends(),
):
    return await supplylinetypeService.list(skip, limit)


# get supplyline type route
@linetypeRouter.get(
    "/{code}",
    summary="Getting router a supply line type without items",
    description="This router allows to get a supply line type without items",
    response_model=SupplyLineTypeSchema,
)
async def get(
    code: int, 
    supplylinetypeService: SupplyLineTypeService = Depends()
):
    supplylinetype = await supplylinetypeService.getbycode(code=code)
    if supplylinetype is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supply Line Type not found",
        )
    return supplylinetype


# post supplyline type route
@linetypeRouter.post(
    "/",
    summary="Creation router a supply line type",
    description="This router allows to create a supply line type",
    response_model=List[CreateSupplyLineType],
    dependencies=[Depends(JWTBearer())]
)
async def create(
    data: List[SupplyLineTypeInput],
    supplylinetypeService: SupplyLineTypeService = Depends(),
):
    return await supplylinetypeService.create(data=data)


# update supplyline type route
@linetypeRouter.put(
    "/{code}",
    summary="Update router a supply line type",
    description="This router allows to update a supply line type",
    response_model=SupplyLineTypeSchema,
    dependencies=[Depends(JWTBearer())]
)
async def update(
    code: int,
    data: SupplyLineTypeUpdate,
    supplylinetypeService: SupplyLineTypeService = Depends(),
):
    return await supplylinetypeService.update(code=code, data=data)