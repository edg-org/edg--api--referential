from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.electrical.services.EnergyDepartureService import (
    EnergyDepartureService,
)
from api.electrical.schemas.EnergyDepartureSchema import (
    EnergyDepartureBase,
    CreateEnergyDeparture,
    EnergyDepartureSchema,
    EnergyDepartureItemSchema,
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

departureRouter = APIRouter(
    prefix=router_path + "/departures",
    tags=["Energy Departures"],
)


# get all energy departures route
@departureRouter.get(
    "/",
    summary="Getting router for all energy departures",
    description="This router allows to get all energy departures",
    response_model=List[EnergyDepartureSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    departureService: EnergyDepartureService = Depends(),
):
    return await departureService.list(skip, limit)


# get energy departure route
@departureRouter.get(
    "/{code}",
    summary="Getting router a energy departure without items",
    description="This router allows to get a energy departure without items",
    response_model=EnergyDepartureSchema,
)
async def get(
    code: int,
    departureService: EnergyDepartureService = Depends(),
):
    departure = await departureService.getbycode(code=code)
    if departure is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Energy Departure not found",
        )
    return departure


# route of get energy departure with item
@departureRouter.get(
    "/items/{code}",
    summary="Getting router a energy departure with items",
    description="This router allows to get a energy departure with items",
    response_model=EnergyDepartureItemSchema,
)
async def get_departure_item(
    code: int,
    departureService: EnergyDepartureService = Depends(),
):
    zone = await departureService.getbycode(code=code)
    if zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Energy Departure not found",
        )
    return zone


# post energy departure route
@departureRouter.post(
    "/",
    summary="Creation router a energy departure",
    description="This router allows to create a energy departure",
    response_model=List[CreateEnergyDeparture],
)
async def create(
    data: List[CreateEnergyDeparture],
    departureService: EnergyDepartureService = Depends(),
):
    return await departureService.create(data=data)


# update energy departure route
@departureRouter.put(
    "/{code}",
    summary="Update router a energy departure",
    description="This router allows to update a energy departure",
    response_model=EnergyDepartureSchema,
)
async def update(
    code: int,
    data: EnergyDepartureBase,
    departureService: EnergyDepartureService = Depends(),
):
    return await departureService.update(
        code=code, data=data
    )
