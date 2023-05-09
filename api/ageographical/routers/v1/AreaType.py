from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.ageographical.services.AreaTypeService import (
    AreaTypeService,
)
from api.ageographical.schemas.AreaTypeSchema import (
    AreaTypeInput,
    CreateAreaType,
    AreaTypeUpdate,
    AreaTypeSchema,
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

areatypeRouter = APIRouter(
    prefix=router_path + "/areatypes", tags=["Area Types"]
)


# get all area types route
@areatypeRouter.get(
    "/",
    summary="Getting router for all area types",
    description="This router allows to get all area types",
    response_model=List[AreaTypeSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    typeService: AreaTypeService = Depends(),
):
    return await typeService.list(skip, limit)


# get area type route
@areatypeRouter.get(
    "/{code}",
    summary="Getting router a area type without items",
    description="This router allows to get a area type without items",
    response_model=AreaTypeSchema,
)
async def get(
    code: int, typeService: AreaTypeService = Depends()
):
    areatype = await typeService.getbycode(code=code)
    if areatype is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Area Type not found",
        )
    return areatype


# post area type route
@areatypeRouter.post(
    "/",
    summary="Creation router a area type",
    description="This router allows to create a area type",
    response_model=List[CreateAreaType],
)
async def create(
    data: List[AreaTypeInput],
    typeService: AreaTypeService = Depends(),
):
    return await typeService.create(data=data)


# update area type route
@areatypeRouter.put(
    "/{code}",
    summary="Update router a area type",
    description="This router allows to update a area type",
    response_model=AreaTypeSchema,
)
async def update(
    code: int,
    data: AreaTypeUpdate,
    typeService: AreaTypeService = Depends(),
):
    return await typeService.update(code=code, data=data)
