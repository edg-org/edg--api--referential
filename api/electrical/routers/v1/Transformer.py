from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.electrical.services.TransformerService import TransformerService
from api.electrical.schemas.TransformerSchema import (
    TransformerInput,
    CreateTransformer,
    TransformerSchema,
    TransformerUpdate,
    TransformerItemSchema
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
    response_model=List[TransformerSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    transformerService: TransformerService = Depends(),
):
    return await transformerService.list(skip, limit)


# get transformer route
@transformerRouter.get(
    "/{code}",
    summary="Getting router a transformer without items",
    description="This router allows to get a transformer without items",
    response_model=TransformerSchema,
)
async def get(
    code: int,
    transformerService: TransformerService = Depends(),
):
    transformer = await transformerService.getbycode(code=code)
    if transformer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transformer not found",
        )
    return transformer


# route of get tranformer with item
@transformerRouter.get(
    "/items/{code}",
    summary="Getting router a transformer with items",
    description="This router allows to get a transformer with items",
    response_model=TransformerItemSchema,
)
async def get_tranformer_item(
    code: int,
    transformerService: TransformerService = Depends(),
):
    transformer = await transformerService.getbycode(code=code)
    if transformer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transformer not found",
        )
    return transformer


# post transformer route
@transformerRouter.post(
    "/",
    summary="Creation router a transformer",
    description="This router allows to create a transformer",
    response_model=List[CreateTransformer],
)
async def create(
    data: List[TransformerInput],
    transformerService: TransformerService = Depends(),
):
    return await transformerService.create(data=data)


# update transformer route
@transformerRouter.put(
    "/{code}",
    summary="Update router a transformer",
    description="This router allows to update a transformer",
    response_model=TransformerSchema,
)
async def update(
    code: int,
    data: TransformerUpdate,
    transformerService: TransformerService = Depends(),
):
    return await transformerService.update(code=code, data=data)