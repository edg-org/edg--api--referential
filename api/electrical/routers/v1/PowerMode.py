from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.electrical.services.PowerModeService import (
    PowerModeService,
)
from api.electrical.schemas.PowerModeSchema import (
    PowerModeBase,
    CreatePowerMode,
    PowerModeSchema,
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

powermodeRouter = APIRouter(
    prefix=router_path + "/powermodes", tags=["Power Modes"]
)


# get all power modes route
@powermodeRouter.get(
    "/",
    summary="Getting router for all power modes",
    description="This router allows to get all power modes",
    response_model=List[PowerModeSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    powerService: PowerModeService = Depends(),
):
    return await powerService.list(skip, limit)


# get power mode route
@powermodeRouter.get(
    "/{code}",
    summary="Getting router a power mode without items",
    description="This router allows to get a power mode without items",
    response_model=PowerModeSchema,
)
async def get(
    code: int, powerService: PowerModeService = Depends()
):
    powermode = await powerService.getbycode(code=code)
    if powermode is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meter Type not found",
        )
    return powermode


# post power mode route
@powermodeRouter.post(
    "/",
    summary="Creation router a power mode",
    description="This router allows to create a power mode",
    response_model=List[CreatePowerMode],
)
async def create(
    data: List[CreatePowerMode],
    powerService: PowerModeService = Depends(),
):
    return await powerService.create(data=data)


# update power mode route
@powermodeRouter.put(
    "/{code}",
    summary="Update router a power mode",
    description="This router allows to update a power mode",
    response_model=PowerModeSchema,
)
async def update(
    code: int,
    data: PowerModeBase,
    powerService: PowerModeService = Depends(),
):
    return await powerService.update(code=code, data=data)
