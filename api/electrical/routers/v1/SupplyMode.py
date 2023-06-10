from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.electrical.services.SupplyModeService import SupplyModeService
from api.electrical.schemas.SupplyModeSchema import (
    SupplyModeInput,
    CreateSupplyMode,
    SupplyModeUpdate,
    SupplyModeSchema
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

supplymodeRouter = APIRouter(
    prefix=router_path + "/supplymodes", tags=["Supply Modes"]
)

# get all supply modes route
@supplymodeRouter.get(
    "/",
    summary="Getting router for all supply modes",
    description="This router allows to get all supply modes",
    response_model=List[SupplyModeSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    supplymodeService: SupplyModeService = Depends(),
):
    return await supplymodeService.list(skip, limit)


# get supply mode route
@supplymodeRouter.get(
    "/{code}",
    summary="Getting router a supply mode without items",
    description="This router allows to get a supply mode without items",
    response_model=SupplyModeSchema,
)
async def get(
    code: int, supplymodeService: SupplyModeService = Depends()
):
    supplymode = await supplymodeService.getbycode(code=code)
    if supplymode is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meter Type not found",
        )
    return supplymode


# post supply mode route
@supplymodeRouter.post(
    "/",
    summary="Creation router a supply mode",
    description="This router allows to create a supply mode",
    response_model=List[CreateSupplyMode],
)
async def create(
    data: List[SupplyModeInput],
    supplymodeService: SupplyModeService = Depends(),
):
    return await supplymodeService.create(data=data)


# update supply mode route
@supplymodeRouter.put(
    "/{code}",
    summary="Update router a supply mode",
    description="This router allows to update a supply mode",
    response_model=SupplyModeSchema,
)
async def update(
    code: int,
    data: SupplyModeUpdate,
    supplymodeService: SupplyModeService = Depends(),
):
    return await supplymodeService.update(code=code, data=data)
