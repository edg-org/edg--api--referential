from typing import List
from api.tools.JWTBearer import JWTBearer, env
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.electrical.services.MeterTypeService import MeterTypeService
from api.electrical.schemas.MeterTypeSchema import (
    MeterTypeInput,
    CreateMeterType,
    MeterTypeUpdate,
    MeterTypeSchema
)

router_path = env.api_routers_prefix + env.api_version

metertypeRouter = APIRouter(
    tags=["Meter Types"],
    prefix=router_path + "/metertypes",
    dependencies=[Depends(JWTBearer())]
)


# get all meter types route
@metertypeRouter.get(
    "/",
    summary="Getting router for all meter types",
    description="This router allows to get all meter types",
    response_model=List[MeterTypeSchema],
)
async def list(
    start: int = 0,
    size: int = 100,
    metertypeService: MeterTypeService = Depends(),
):
    return await metertypeService.list(start, size)


# get meter type route
@metertypeRouter.get(
    "/{code}",
    summary="Getting router a meter type without items",
    description="This router allows to get a meter type without items",
    response_model=MeterTypeSchema
)
async def get(
    code: int, 
    metertypeService: MeterTypeService = Depends()
):
    metertype = await metertypeService.getbycode(code=code)
    if metertype is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meter Type not found",
        )
    return metertype


# post meter type route
@metertypeRouter.post(
    "/",
    summary="Creation router a meter type",
    description="This router allows to create a meter type",
    response_model=List[CreateMeterType]
)
async def create(
    data: List[MeterTypeInput],
    metertypeService: MeterTypeService = Depends(),
):
    return await metertypeService.create(data=data)

# update meter type route
@metertypeRouter.put(
    "/{code}",
    summary="Update router a meter type",
    description="This router allows to update a meter type",
    response_model=MeterTypeSchema
)
async def update(
    code: int,
    data: MeterTypeUpdate,
    metertypeService: MeterTypeService = Depends(),
    tokendata: dict = Depends(JWTBearer())
):
    return await metertypeService.update(code=code, tokendata=tokendata, data=data)