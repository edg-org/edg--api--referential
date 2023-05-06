from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.electrical.services.TransformerService import (
    TransformerService,
)
from api.electrical.schemas.TransformerSchema import (
    TransformerBase,
    CreateTransformer,
    TransformerSchema,
    TransformerItemSchema,
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

transformerRouter = APIRouter(
    prefix=router_path + "/transformers",
    tags=["Transformers"],
)


# get all transformers route
@transformerRouter.get(
    "/",
    summary="Getting router for all transformers",
    description="This router allows to get all transformers",
    # response_model=List[TransformerSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    transformerService: TransformerService = Depends(),
):
    return await transformerService.list(skip, limit)


# get transformer route
@transformerRouter.get(
    "/{number}",
    summary="Getting router a transformer without items",
    description="This router allows to get a transformer without items",
    response_model=TransformerSchema,
)
async def get(
    number: str,
    transformerService: TransformerService = Depends(),
):
    departure = await transformerService.getbynumber(
        number=number
    )
    if departure is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transformer not found",
        )
    return departure


# route of get tranformer with item
@transformerRouter.get(
    "/items/{number}",
    summary="Getting router a transformer with items",
    description="This router allows to get a transformer with items",
    response_model=TransformerItemSchema,
)
async def get_tranformer_item(
    number: str,
    transformerService: TransformerService = Depends(),
):
    zone = await transformerService.getbynumber(
        number=number
    )
    if zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transformer not found",
        )
    return zone


# post transformer route
@transformerRouter.post(
    "/",
    summary="Creation router a transformer",
    description="This router allows to create a transformer",
    response_model=List[CreateTransformer],
)
async def create(
    data: List[CreateTransformer],
    transformerService: TransformerService = Depends(),
):
    return await transformerService.create(data=data)


# update transformer route
@transformerRouter.put(
    "/{number}",
    summary="Update router a transformer",
    description="This router allows to update a transformer",
    response_model=TransformerSchema,
)
async def update(
    number: str,
    data: TransformerBase,
    transformerService: TransformerService = Depends(),
):
    return await transformerService.update(
        number=number, data=data
    )
