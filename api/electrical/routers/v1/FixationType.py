from typing import List
from api.tools.JWTBearer import JWTBearer, env
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException,
)
from api.electrical.services.FixationTypeService import FixationTypeService
from api.electrical.schemas.FixationTypeSchema import (
    FixationTypeInput,
    CreateFixationType,
    FixationTypeUpdate,
    FixationTypeSchema
)

router_path = env.api_routers_prefix + env.api_version

fixationtypeRouter = APIRouter(
    tags=["Transformer Fixation Types"],
    prefix=router_path + "/fixationtypes",
    dependencies=[Depends(JWTBearer())]
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
    fixationtypeService: FixationTypeService = Depends(),
):
    return await fixationtypeService.list(skip, limit)

# get fixation type route
@fixationtypeRouter.get(
    "/{code}",
    summary="Getting router a transformer fixation type without items",
    description="This router allows to get a tranformer fixation type without items",
    response_model=FixationTypeSchema,
)
async def get(
    code: int, 
    fixationtypeService: FixationTypeService = Depends()
):
    fixation = await fixationtypeService.getbycode(code=code)
    if fixation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transformer Fixation Type not found",
        )
    return fixation

# post fixation type route
@fixationtypeRouter.post(
    "/",
    summary="Creation router a transformer fixation type",
    description="This router allows to create a tranformer fixation type",
    response_model=List[CreateFixationType],
)
async def create(
    data: List[FixationTypeInput],
    fixationtypeService: FixationTypeService = Depends(),
):
    return await fixationtypeService.create(data=data)


# update fixation type route
@fixationtypeRouter.put(
    "/{code}",
    summary="Update router a transfomer fixation type",
    description="This router allows to update a tranformer fixation type",
    response_model=FixationTypeSchema
)
async def update(
    code: int,
    data: FixationTypeUpdate,
    fixationtypeService: FixationTypeService = Depends(),
    tokendata: dict = Depends(JWTBearer())
):
    return await fixationtypeService.update(code=code, tokendata=tokendata, data=data)