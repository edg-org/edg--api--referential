from typing import List
from api.tools.JWTBearer import JWTBearer, env
from api.salesfinancial.services.ContactTypeService import ContactTypeService
from fastapi import (
    Depends,
    status,
    APIRouter,
    HTTPException
)
from api.salesfinancial.schemas.ContactTypeSchema import (
    CreateContactType,
    ContactTypeUpdate,
    ContactTypeSchema
)

router_path = env.api_routers_prefix + env.api_version
contacttypeRouter = APIRouter(
    tags=["Contact Types"],
    prefix=router_path + "/contacttypes",
    dependencies=[Depends(JWTBearer())]
)

# get all contact types route
@contacttypeRouter.get(
    "/",
    summary="Getting router for all contact types",
    description="This router allows to get all contact types",
    response_model=List[ContactTypeSchema]
)
async def list(
    skip: int = 0,
    limit: int = 100,
    typeService: ContactTypeService = Depends(),
):
    return await typeService.list(skip, limit)

# get contact type route
@contacttypeRouter.get(
    "/{code}",
    summary="Getting router a contact type without items",
    description="This router allows to get a contact type without items",
    response_model=ContactTypeSchema
)
async def get(
    code: int, 
    typeService: ContactTypeService = Depends()
):
    contacttype = await typeService.getbycode(code=code)
    if contacttype is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact Type not found",
        )
    return contacttype

# post contact type route
@contacttypeRouter.post(
    "/",
    summary="Creation router a contact type",
    description="This router allows to create a contact type",
    response_model=List[CreateContactType]
)
async def create(
    data: List[CreateContactType],
    typeService: ContactTypeService = Depends(),
):
    return await typeService.create(data=data)

# update contact type route
@contacttypeRouter.put(
    "/{code}",
    summary="Update router a contact type",
    description="This router allows to update a contact type",
    response_model=ContactTypeSchema
)
async def update(
    code: int,
    data: ContactTypeUpdate,
    typeService: ContactTypeService = Depends(),
    tokendata: dict = Depends(JWTBearer())
):
    return await typeService.update(code=code, tokendata=tokendata, data=data)