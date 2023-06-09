from typing import List
from api.tools.JWTBearer import JWTBearer, env
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
    AgencyPagination
)

router_path = env.api_routers_prefix + env.api_version

agencyRouter = APIRouter(
    tags=["Agencies"],
    prefix=router_path + "/agencies",
    dependencies=[Depends(JWTBearer())]
)

# get all agencies route
@agencyRouter.get(
    "/",
    summary="Getting router for all agencies",
    description="This router allows to get all agencies",
    response_model=AgencyPagination,
)
async def list(
    start: int = 0,
    size: int = 100,
    agencyService: AgencyService = Depends(),
):
    count, agencies = await agencyService.list(start, size)
    return {
        "results": [agency for agency in agencies],
        "total": len(agencies),
        "count": count,
        "page_size": size,
        "start_index": start
    }

# get agency route
@agencyRouter.get(
    "/{code}",
    summary="Getting router a agency without items",
    description="This router allows to get a agency without items",
    response_model=AgencySchema,
)
async def get(
    code: int, 
    agencyService: AgencyService = Depends()
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
    response_model=List[CreateAgency]
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
    response_model=AgencySchema
)
async def update(
    code: int,
    data: AgencyUpdate,
    agencyService: AgencyService = Depends(),
    tokendata: dict = Depends(JWTBearer())
):
    return await agencyService.update(code=code, tokendata=tokendata, data=data)