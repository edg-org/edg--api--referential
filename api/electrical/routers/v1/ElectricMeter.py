from typing import List
from api.tools.JWTBearer import JWTBearer, env
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.electrical.services.ElectricMeterService import ElectricMeterService
from api.electrical.schemas.ElectricMeterSchema import (
    ElectricMeterInput,
    CreateElectricMeter,
    ElectricMeterUpdate,
    ElectricMeterSchema,
    ElectricMeterPagination
)

router_path = env.api_routers_prefix + env.api_version

meterRouter = APIRouter(
    tags=["Electric Meters"],
    prefix=router_path + "/meters",
    dependencies=[Depends(JWTBearer())]
)

# get all electric meter route
@meterRouter.get(
    "/",
    summary="Getting router for all electric meters",
    description="This router allows to get all electric meters",
    response_model=ElectricMeterPagination
)
async def list(
    start: int = 0,
    size: int = 100,
    meterService: ElectricMeterService = Depends(),
):
    count, meters = await meterService.list(start, size)
    return {
        "results": [meter for meter in meters],
        "total": len(meters),
        "count": count,
        "page_size": size,
        "start_index": start
    }


# get transformer route
@meterRouter.get(
    "/{number}",
    summary="Getting router a transformer without items",
    description="This router allows to get a electric meter without items",
    response_model=ElectricMeterSchema,
)
async def get(
    number: int,
    meterService: ElectricMeterService = Depends(),
):
    supply = await meterService.getbynumber(number=number)
    if supply is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Electric Meter not found",
        )
    return supply

# post transformer route
@meterRouter.post(
    "/",
    summary="Creation router a electric meter",
    description="This router allows to create a electric meter",
    response_model=List[CreateElectricMeter]
)
async def create(
    data: List[ElectricMeterInput],
    meterService: ElectricMeterService = Depends(),
):
    return await meterService.create(data=data)

# update transformer route
@meterRouter.put(
    "/{number}",
    summary="Update router a electric meter",
    description="This router allows to update a electric meter",
    response_model=ElectricMeterSchema
)
async def update(
    number: int,
    data: ElectricMeterUpdate,
    meterService: ElectricMeterService = Depends(),
    tokendata: dict = Depends(JWTBearer())
):
    return await meterService.update(number=number, tokendata=tokendata, data=data)