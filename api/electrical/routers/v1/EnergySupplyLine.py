from typing import List
from api.tools.JWTBearer import JWTBearer, env
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.electrical.services.EnergySupplyLineService import EnergySupplyLineService
from api.electrical.schemas.EnergySupplyLineSchema import (
    EnergySupplyLineInput,
    CreateEnergySupplyLine,
    EnergySupplyLineSchema,
    EnergySupplyLineUpdate
)

router_path = env.api_routers_prefix + env.api_version

energysupplyRouter = APIRouter(
    tags=["Energy Supply Lines"],
    prefix=router_path + "/supplylines"
)

# get all energy supply line lines route
@energysupplyRouter.get(
    "/",
    summary="Getting router for all energy supply lines",
    description="This router allows to get all energy supply line lines",
    response_model=List[EnergySupplyLineSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    energysupplyService: EnergySupplyLineService = Depends(),
):
    return await energysupplyService.list(skip, limit)


# get energy supply line route
@energysupplyRouter.get(
    "/{code}",
    summary="Getting router a energy supply line without items",
    description="This router allows to get a energy supply line without items",
    response_model=EnergySupplyLineSchema,
)
async def get(
    code: int,
    energysupplyService: EnergySupplyLineService = Depends(),
):
    energysupply = await energysupplyService.getbycode(code=code)
    if energysupply is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Energy Departure not found",
        )
    return energysupply

# post energy supply line route
@energysupplyRouter.post(
    "/",
    summary="Creation router a energy supply line",
    description="This router allows to create a energy supply line",
    response_model=List[CreateEnergySupplyLine],
    dependencies=[Depends(JWTBearer())]
)
async def create(
    data: List[EnergySupplyLineInput],
    energysupplyService: EnergySupplyLineService = Depends(),
):
    return await energysupplyService.create(data=data)


# update energy supply line route
@energysupplyRouter.put(
    "/{code}",
    summary="Update router a energy supply line",
    description="This router allows to update a energy supply line",
    response_model=EnergySupplyLineSchema,
    dependencies=[Depends(JWTBearer())]
)
async def update(
    code: int,
    data: EnergySupplyLineUpdate,
    energysupplyService: EnergySupplyLineService = Depends(),
):
    return await energysupplyService.update(code=code, data=data)