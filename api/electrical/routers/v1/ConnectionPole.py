from typing import List
from api.tools.JWTBearer import JWTBearer, env
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.electrical.services.ConnectionPoleService import ConnectionPoleService
from api.electrical.schemas.ConnectionPoleSchema import (
    ConnectionPoleInput,
    CreateConnectionPole,
    ConnectionPoleSchema,
    ConnectionPoleUpdate,
    ConnectionPoleItemSchema
)

router_path = env.api_routers_prefix + env.api_version

poleRouter = APIRouter(
    tags=["Connection Poles"],
    prefix=router_path + "/connectionpoles"
)

# get all connection poles route
@poleRouter.get(
    "/",
    summary="Getting router for all connection poles",
    description="This router allows to get all connection poles ",
    response_model=List[ConnectionPoleSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    poleService: ConnectionPoleService = Depends(),
):
    return await poleService.list(skip, limit)

# get transformer route
@poleRouter.get(
    "/{number}",
    summary="Getting router a connection pole without items",
    description="This router allows to get a connection pole without items",
    response_model=ConnectionPoleSchema,
)
async def get(
    number: int,
    poleService: ConnectionPoleService = Depends(),
):
    pole = await poleService.getbynumber(
        number=number
    )
    if pole is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection Pole not found",
        )
    return pole

# route of get tranformer with item
@poleRouter.get(
    "/{number}/items",
    summary="Getting router a connection pole with items",
    description="This router allows to get a connection pole with items",
    response_model=ConnectionPoleItemSchema,
)
async def get_tranformer_item(
    number: int,
    poleService: ConnectionPoleService = Depends(),
):
    pole = await poleService.getbynumber(
        number=number
    )
    if pole is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection Pole not found",
        )
    return pole

# post transformer route
@poleRouter.post(
    "/",
    summary="Creation router a connection pole",
    description="This router allows to create a connection pole",
    response_model=List[CreateConnectionPole],
    dependencies=[Depends(JWTBearer())]
)
async def create(
    data: List[ConnectionPoleInput],
    poleService: ConnectionPoleService = Depends(),
):
    return await poleService.create(data=data)

# update transformer route
@poleRouter.put(
    "/{number}",
    summary="Update router a connection pole",
    description="This router allows to update a connection pole",
    response_model=ConnectionPoleSchema,
    dependencies=[Depends(JWTBearer())]
)
async def update(
    number: int,
    data: ConnectionPoleUpdate,
    poleService: ConnectionPoleService = Depends(),
):
    return await poleService.update(number=number, data=data)