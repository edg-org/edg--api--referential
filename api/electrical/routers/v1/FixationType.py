from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.electrical.services.FixationTypeService import FixationTypeService
from api.electrical.schemas.FixationTypeSchema import (
    FixationTypeInput,
    CreateFixationType,
    FixationTypeUpdate,
    FixationTypeSchema
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

fixationtypeRouter = APIRouter(
    prefix=router_path + "/fixationtypes", tags=["Transformer Fixation Types"]
)

# get all fixation types route
@fixationtypeRouter.get(
    "/",
    summary="Getting router for all transfomer fixation types",
    description="This router allows to get all tranformer fixation types",
    response_model=List[FixationTypeSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    supplylineService: FixationTypeService = Depends(),
):
    return await supplylineService.list(skip, limit)


# get fixation type route
@fixationtypeRouter.get(
    "/{code}",
    summary="Getting router a transformer fixation type without items",
    description="This router allows to get a tranformer fixation type without items",
    response_model=FixationTypeSchema,
)
async def get(
    code: int, supplylineService: FixationTypeService = Depends()
):
    supplyline = await supplylineService.getbycode(code=code)
    if supplylinetype is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transformer Fixation Type not found",
        )
    return supplyline


# post fixation type route
@fixationtypeRouter.post(
    "/",
    summary="Creation router a transformer fixation type",
    description="This router allows to create a tranformer fixation type",
    response_model=List[CreateFixationType],
)
async def create(
    data: List[FixationTypeInput],
    supplylineService: FixationTypeService = Depends(),
):
    return await supplylineService.create(data=data)


# update fixation type route
@fixationtypeRouter.put(
    "/{code}",
    summary="Update router a transfomer fixation type",
    description="This router allows to update a tranformer fixation type",
    response_model=FixationTypeSchema,
)
async def update(
    code: int,
    data: FixationTypeUpdate,
    supplylineService: FixationTypeService = Depends(),
):
    return await supplylineService.update(code=code, data=data)