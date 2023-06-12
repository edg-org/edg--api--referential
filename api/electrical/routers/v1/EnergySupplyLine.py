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
    EnergySupplyLineUpdate,
    ElectricSupplyLinePagination
)

router_path = env.api_routers_prefix + env.api_version

energysupplyRouter = APIRouter(
    tags=["Energy Supply Lines"],
    prefix=router_path + "/supplylines",
    dependencies=[Depends(JWTBearer())]
)

# get all energy supply line lines route
@energysupplyRouter.get(
    "/",
    summary="Getting router for all energy supply lines",
    description="This router allows to get all energy supply line lines",
    response_model=ElectricSupplyLinePagination,
)
async def list(
    start: int = 0,
    size: int = 100,
    lineService: EnergySupplyLineService = Depends(),
):
    count, lines = await lineService.list(start, size)
    return {
        "results": [line for line in lines],
        "total": len(lines),
        "count": count,
        "page_size": size,
        "start_index": start
    }


# get energy supply line route
@energysupplyRouter.get(
    "/{code}",
    summary="Getting router a energy supply line without items",
    description="This router allows to get a energy supply line without items",
    response_model=EnergySupplyLineSchema,
)
async def get(
    code: int,
    lineService: EnergySupplyLineService = Depends(),
):
    energysupply = await lineService.getbycode(code=code)
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
    response_model=List[CreateEnergySupplyLine]
)
async def create(
    data: List[EnergySupplyLineInput],
    lineService: EnergySupplyLineService = Depends(),
):
    return await lineService.create(data=data)

# update energy supply line route
@energysupplyRouter.put(
    "/{code}",
    summary="Update router a energy supply line",
    description="This router allows to update a energy supply line",
    response_model=EnergySupplyLineSchema,
)
async def update(
    code: int,
    data: EnergySupplyLineUpdate,
    lineService: EnergySupplyLineService = Depends(),
    tokendata: dict = Depends(JWTBearer())
):
    return await lineService.update(code=code, tokendata=tokendata, data=data)