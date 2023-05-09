from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.ageographical.services.PrefectureService import (
    PrefectureService,
)
from api.ageographical.schemas.PrefectureSchema import (
    PrefectureInput,
    PrefectureSchema,
    PrefectureUpdate,
    CreatePrefecture,
    PrefectureItemSchema,
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

prefectureRouter = APIRouter(
    prefix=router_path + "/prefectures",
    tags=["Prefectures"],
)


# get all prefectures route
@prefectureRouter.get(
    "/",
    summary="Getting router for all prefectures",
    description="This router allows to get all prefectures",
    response_model=List[PrefectureSchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    prefectureService: PrefectureService = Depends(),
):
    return await prefectureService.list(skip, limit)


# get prefecture route
@prefectureRouter.get(
    "/{code}",
    summary="Getting router a prefecture without items",
    description="This router allows to get a prefecture without items",
    response_model=PrefectureSchema,
)
async def get(
    code: int,
    prefectureService: PrefectureService = Depends(),
):
    prefecture = await prefectureService.getbycode(
        code=code
    )
    if prefecture is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prefecture not found",
        )
    return prefecture


# route of get prefecture with item
@prefectureRouter.get(
    "/items/{code}",
    summary="Getting router a prefecture with items",
    description="This router allows to get a prefecture with items",
    response_model=PrefectureItemSchema,
)
async def get_prefecture_item(
    code: int,
    prefectureService: PrefectureService = Depends(),
):
    prefecture = await prefectureService.getbycode(
        code=code
    )
    if prefecture is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prefecture not found",
        )
    return prefecture


# post prefecture route
@prefectureRouter.post(
    "/",
    summary="Creation router a prefecture",
    description="This router allows to create a prefecture",
    response_model=List[CreatePrefecture],
)
async def create(
    data: List[PrefectureInput],
    prefectureService: PrefectureService = Depends(),
):
    return await prefectureService.create(data=data)


# update prefecture route
@prefectureRouter.put(
    "/{code}",
    summary="Update router a prefecture",
    description="This router allows to update a prefecture",
    response_model=PrefectureSchema,
)
async def update(
    code: int,
    data: PrefectureUpdate,
    prefectureService: PrefectureService = Depends(),
):
    return await prefectureService.update(
        code=code, data=data
    )
