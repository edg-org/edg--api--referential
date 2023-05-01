from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, Query, Body, Path, Header, Cookie, Form, File

from api.schemas.pydantic.RefRegionalDelegationsSchema import (RefRegionalDelegationsSchema, RefRegionalDelegationsCreateSchema,
RefRegionalDelegationsUpdateSchema, EXAMPLE, EXAMPLE1)
from api.services.RefRegionalDelegationsService import RefRegionalDelegationsService

RefRegionalDelegationsRouter = APIRouter(prefix="/v1/regionaldelegation", tags=["Regional Delegations"])

@RefRegionalDelegationsRouter.get("/", response_model = List[RefRegionalDelegationsSchema])
def index(skip: Optional[int] = 0, limit: Optional[int] = 100, refRegionalDelegations: RefRegionalDelegationsService = Depends()):
    return jsonable_encoder(refRegionalDelegations.list(skip,limit))

# @RefRegionalDelegationsRouter.get("/{id}")
@RefRegionalDelegationsRouter.get("/{id}", response_model = RefRegionalDelegationsSchema)
def get(id: int, refRegionalDelegations: RefRegionalDelegationsService = Depends()):
    return refRegionalDelegations.get(id)
    # return jsonable_encoder(refRegionalDelegations.get(id))

@RefRegionalDelegationsRouter.post("/", response_model = RefRegionalDelegationsSchema, status_code = status.HTTP_201_CREATED)
def create(refRegionalDelegation: RefRegionalDelegationsCreateSchema = Body(example = EXAMPLE), refRegionalDelegations: RefRegionalDelegationsService = Depends()):
# def create(refRegionalDelegation: RefRegionalDelegationsCreateSchema = Body(), refRegionalDelegations: RefRegionalDelegationsService = Depends()):
    refRegionalDelegation = refRegionalDelegations.create(refRegionalDelegation)
    return refRegionalDelegation 

@RefRegionalDelegationsRouter.put("/", response_model = RefRegionalDelegationsSchema)
# @RefRegionalDelegationsRouter.put("/")
def update(refRegionalDelegation: RefRegionalDelegationsUpdateSchema = Body(example = EXAMPLE1), refRegionalDelegations: RefRegionalDelegationsService = Depends()):
# def update(refRegionalDelegation: RefRegionalDelegationsUpdateSchema = Body(), refRegionalDelegations: RefRegionalDelegationsService = Depends()):
    return refRegionalDelegations.update(refRegionalDelegation)

@RefRegionalDelegationsRouter.delete("/{id}", response_model = RefRegionalDelegationsSchema)
# @RefRegionalDelegationsRouter.delete("/{id}")
def delete(id: int, refRegionalDelegations: RefRegionalDelegationsService = Depends()):
    return refRegionalDelegations.delete(id)

@RefRegionalDelegationsRouter.put("/restore/{id}", response_model = RefRegionalDelegationsSchema)
# @RefRegionalDelegationsRouter.put("/restore/{id}")
def restore(id: int, refRegionalDelegations: RefRegionalDelegationsService = Depends()):
    return refRegionalDelegations.retaure(id)

# @RefRegionalDelegationsRouter.delete("/{id}/{signature}")
@RefRegionalDelegationsRouter.delete("/{id}/{signature}", response_model = RefRegionalDelegationsSchema)
def delete_signature(id: int, signature: str, refRegionalDelegations: RefRegionalDelegationsService = Depends()):
    return refRegionalDelegations.delete_signature(id, signature)

@RefRegionalDelegationsRouter.get("/items/")
def get_items(id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, refRegionalDelegations: RefRegionalDelegationsService = Depends()):
    return refRegionalDelegations.get_items(id, code, signature)

