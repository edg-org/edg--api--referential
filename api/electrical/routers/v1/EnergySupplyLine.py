from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.electrical.services.EnergySupplyLineService import EnergySupplyLineService
from api.electrical.schemas.EnergySupplyLineSchema import (
    EnergySupplyLineInput,
    CreateEnergySupplyLine,
    EnergySupplyLineSchema,
    EnergySupplyLineUpdate,
    EnergySupplyLineItemSchema
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

supplyRouter = APIRouter(
    prefix=router_path + "/supplylines",
    tags=["Energy Supply Lines"],
)


# get all energy supply line lines route
@supplyRouter.get(
    "/",
    summary="Getting router for all energy supply lines",
    description="This router allows to get all energy supply line lines",
    response_model=List[EnergySupplyLineSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    supplyService: EnergySupplyLineService = Depends(),
):
    return await supplyService.list(skip, limit)


# get energy supply line route
@supplyRouter.get(
    "/{code}",
    summary="Getting router a energy supply line without items",
    description="This router allows to get a energy supply line without items",
    response_model=EnergySupplyLineSchema,
)
async def get(
    code: int,
    supplyService: EnergySupplyLineService = Depends(),
):
    supply = await supplyService.getbycode(code=code)
    if supply is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Energy Departure not found",
        )
    return supply


# route of get energy supply line with item
@supplyRouter.get(
    "/items/{code}",
    summary="Getting router a energy supply line with items",
    description="This router allows to get a energy supply line with items",
    response_model=EnergySupplyLineItemSchema,
)
async def get_supply_item(
    code: int,
    supplyService: EnergySupplyLineService = Depends(),
):
    zone = await supplyService.getbycode(code=code)
    if zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Energy Departure not found",
        )
    return zone


# post energy supply line route
@supplyRouter.post(
    "/",
    summary="Creation router a energy supply line",
    description="This router allows to create a energy supply line",
    response_model=List[CreateEnergySupplyLine],
)
async def create(
    data: List[EnergySupplyLineInput],
    supplyService: EnergySupplyLineService = Depends(),
):
    return await supplyService.create(data=data)


# update energy supply line route
@supplyRouter.put(
    "/{code}",
    summary="Update router a energy supply line",
    description="This router allows to update a energy supply line",
    response_model=EnergySupplyLineSchema,
)
async def update(
    code: int,
    data: EnergySupplyLineUpdate,
    supplyService: EnergySupplyLineService = Depends(),
):
    return await supplyService.update(
        code=code, data=data
    )
