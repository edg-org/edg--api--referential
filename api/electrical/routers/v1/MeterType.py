from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.electrical.services.MeterTypeService import (
    MeterTypeService,
)
from api.electrical.schemas.MeterTypeSchema import (
    MeterTypeBase,
    CreateMeterType,
    MeterTypeSchema,
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

metertypeRouter = APIRouter(
    prefix=router_path + "/metertypes", tags=["Meter Types"]
)


# get all meter types route
@metertypeRouter.get(
    "/",
    summary="Getting router for all meter types",
    description="This router allows to get all meter types",
    response_model=List[MeterTypeSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    typeService: MeterTypeService = Depends(),
):
    return await typeService.list(skip, limit)


# get meter type route
@metertypeRouter.get(
    "/{code}",
    summary="Getting router a meter type without items",
    description="This router allows to get a meter type without items",
    response_model=MeterTypeSchema,
)
async def get(
    code: int, typeService: MeterTypeService = Depends()
):
    metertype = await typeService.getbycode(code=code)
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
    response_model=List[CreateMeterType],
)
async def create(
    data: List[CreateMeterType],
    typeService: MeterTypeService = Depends(),
):
    return await typeService.create(data=data)


# update meter type route
@metertypeRouter.put(
    "/{code}",
    summary="Update router a meter type",
    description="This router allows to update a meter type",
    response_model=MeterTypeSchema,
)
async def update(
    code: int,
    data: MeterTypeBase,
    typeService: MeterTypeService = Depends(),
):
    return await typeService.update(code=code, data=data)
