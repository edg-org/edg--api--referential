from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.ageographical.services.AgencyService import AgencyService
from api.ageographical.schemas.AgencySchema import (
    AgencyInput,
    CreateAgency,
    AgencyUpdate,
    AgencySchema,
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

agencyRouter = APIRouter(
    prefix=router_path + "/agencies", tags=["Agencies"]
)

# get all agencies route
@agencyRouter.get(
    "/",
    summary="Getting router for all agencies",
    description="This router allows to get all agencies",
    response_model=List[AgencySchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    agencyService: AgencyService = Depends(),
):
    return await agencyService.list(skip, limit)

# get agency route
@agencyRouter.get(
    "/{code}",
    summary="Getting router a agency without items",
    description="This router allows to get a agency without items",
    response_model=AgencySchema,
)
async def get(
    code: int, agencyService: AgencyService = Depends()
):
    agency = await agencyService.getbycode(code=code)
    if agency is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agency not found",
        )
    return agency

# post agency route
@agencyRouter.post(
    "/",
    summary="Creation router a agency",
    description="This router allows to create a agency",
    response_model=List[CreateAgency],
)
async def create(
    data: List[AgencyInput],
    agencyService: AgencyService = Depends(),
):
    return await agencyService.create(data=data)


# update agency route
@agencyRouter.put(
    "/{code}",
    summary="Update router a agency",
    description="This router allows to update a agency",
    response_model=AgencySchema,
)
async def update(
    code: int,
    data: AgencyUpdate,
    agencyService: AgencyService = Depends(),
):
    return await agencyService.update(code=code, data=data)
