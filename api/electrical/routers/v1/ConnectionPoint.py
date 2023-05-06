from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.electrical.services.ConnectionPointService import (
    ConnectionPointService,
)
from api.electrical.schemas.ConnectionPointSchema import (
    ConnectionPointBase,
    CreateConnectionPoint,
    ConnectionPointSchema,
    ConnectionPointItemSchema,
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

connectionRouter = APIRouter(
    prefix=router_path + "/connectionpoints",
    tags=["Connection Points"],
)


# get all connection points route
@connectionRouter.get(
    "/",
    summary="Getting router for all connection points",
    description="This router allows to get all connection points ",
    # response_model=List[ConnectionPointSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    connectionService: ConnectionPointService = Depends(),
):
    return await connectionService.list(skip, limit)


# get transformer route
@connectionRouter.get(
    "/{number}",
    summary="Getting router a transformer without items",
    description="This router allows to get a connection point without items",
    response_model=ConnectionPointSchema,
)
async def get(
    number: int,
    connectionService: ConnectionPointService = Depends(),
):
    departure = await connectionService.getbynumber(
        number=number
    )
    if departure is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection Point not found",
        )
    return departure


# route of get tranformer with item
@connectionRouter.get(
    "/items/{number}",
    summary="Getting router a transformer with items",
    description="This router allows to get a transformer with items",
    response_model=ConnectionPointItemSchema,
)
async def get_tranformer_item(
    number: int,
    connectionService: ConnectionPointService = Depends(),
):
    zone = await connectionService.getbynumber(
        number=number
    )
    if zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection Point not found",
        )
    return zone


# post transformer route
@connectionRouter.post(
    "/",
    summary="Creation router a connection point",
    description="This router allows to create a connection point",
    response_model=List[CreateConnectionPoint],
)
async def create(
    data: List[CreateConnectionPoint],
    connectionService: ConnectionPointService = Depends(),
):
    return await connectionService.create(data=data)


# update transformer route
@connectionRouter.put(
    "/{number}",
    summary="Update router a connection point",
    description="This router allows to update a connection point",
    response_model=ConnectionPointSchema,
)
async def update(
    number: int,
    data: ConnectionPointBase,
    connectionService: ConnectionPointService = Depends(),
):
    return await connectionService.update(
        number=number, data=data
    )
