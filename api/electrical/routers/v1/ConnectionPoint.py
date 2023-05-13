from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.electrical.services.ConnectionPointService import ConnectionPointService
from api.electrical.schemas.ConnectionPointSchema import (
    ConnectionPointInput,
    CreateConnectionPoint,
    ConnectionPointSchema,
    ConnectionPointUpdate,
    ConnectionPointItemSchema
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

connectionpointRouter = APIRouter(
    prefix=router_path + "/connectionpoints",
    tags=["Connection Points"],
)

# get all connection points route
@connectionpointRouter.get(
    "/",
    summary="Getting router for all connection points",
    description="This router allows to get all connection points ",
    response_model=List[ConnectionPointSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    connectionpointService: ConnectionPointService = Depends(),
):
    return await connectionpointService.list(skip, limit)

# get transformer route
@connectionpointRouter.get(
    "/{number}",
    summary="Getting router a transformer without items",
    description="This router allows to get a connection point without items",
    response_model=ConnectionPointSchema,
)
async def get(
    number: int,
    connectionpointService: ConnectionPointService = Depends(),
):
    connectionpoint = await connectionpointService.getbynumber(
        number=number
    )
    if connectionpoint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection Point not found",
        )
    return connectionpoint

# route of get tranformer with item
@connectionpointRouter.get(
    "/items/{number}",
    summary="Getting router a transformer with items",
    description="This router allows to get a transformer with items",
    response_model=ConnectionPointItemSchema,
)
async def get_tranformer_item(
    number: int,
    connectionpointService: ConnectionPointService = Depends(),
):
    connectionpoint = await connectionpointService.getbynumber(
        number=number
    )
    if connectionpoint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection Point not found",
        )
    return connectionpoint

# post transformer route
@connectionpointRouter.post(
    "/",
    summary="Creation router a connection point",
    description="This router allows to create a connection point",
    response_model=List[CreateConnectionPoint],
)
async def create(
    data: List[ConnectionPointInput],
    connectionpointService: ConnectionPointService = Depends(),
):
    return await connectionpointService.create(data=data)

# update transformer route
@connectionpointRouter.put(
    "/{number}",
    summary="Update router a connection point",
    description="This router allows to update a connection point",
    response_model=ConnectionPointSchema,
)
async def update(
    number: int,
    data: ConnectionPointUpdate,
    connectionpointService: ConnectionPointService = Depends(),
):
    return await connectionpointService.update(number=number, data=data)