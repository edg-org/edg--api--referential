from typing import List
from api.tools.JWTBearer import JWTBearer, env
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.electrical.services.VoltageTypeService import VoltageTypeService
from api.electrical.schemas.VoltageTypeSchema import (
    VoltageTypeInput,
    CreateVoltageType,
    VoltageTypeUpdate,
    VoltageTypeSchema
)

router_path = env.api_routers_prefix + env.api_version

voltagetypeRouter = APIRouter(
    tags=["Supply Line Voltage Types"],
    prefix=router_path + "/voltagetypes"
)

# get all voltage types route
@voltagetypeRouter.get(
    "/",
    summary="Getting router for all supply line voltage types",
    description="This router allows to get all supply line voltage types",
    response_model=List[VoltageTypeSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    voltagetypeService: VoltageTypeService = Depends(),
):
    return await voltagetypeService.list(skip, limit)


# get voltage type route
@voltagetypeRouter.get(
    "/{code}",
    summary="Getting router a supply line voltage type without items",
    description="This router allows to get a supply line voltage type without items",
    response_model=VoltageTypeSchema,
)
async def get(
    code: int, voltagetypeService: VoltageTypeService = Depends()
):
    voltagetype = await voltagetypeService.getbycode(code=code)
    if voltagetype is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supply Line Voltage Type not found",
        )
    return voltagetype


# post voltage type route
@voltagetypeRouter.post(
    "/",
    summary="Creation router a supply line voltage type",
    description="This router allows to create a supply line voltage type",
    response_model=List[CreateVoltageType],
    dependencies=[Depends(JWTBearer())]
)
async def create(
    data: List[VoltageTypeInput],
    voltagetypeService: VoltageTypeService = Depends(),
):
    return await voltagetypeService.create(data=data)


# update voltage type route
@voltagetypeRouter.put(
    "/{code}",
    summary="Update router a supply line voltage type",
    description="This router allows to update a supply line voltage type",
    response_model=VoltageTypeSchema,
    dependencies=[Depends(JWTBearer())]
)
async def update(
    code: int,
    data: VoltageTypeUpdate,
    voltagetypeService: VoltageTypeService = Depends(),
):
    return await voltagetypeService.update(code=code, data=data)