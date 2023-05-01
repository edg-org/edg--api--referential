from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, Query, Body, Path, Header, Cookie, Form, File

from api.schemas.pydantic.RefCitiesSchema import RefCitiesSchema, RefCitiesCreateSchema
from api.schemas.pydantic.RefAgenciesSchema import (RefAgenciesSchema, RefAgenciesCreateSchema, EXAMPLE, RefAgenciesUpdateSchema,
EXAMPLE1)

from api.services.RefAgenciesService import RefAgenciesService


RefAgenciesRouter = APIRouter(prefix="/v1/agency", tags=["Agencies"])

@RefAgenciesRouter.get("/", response_model=List[RefAgenciesSchema])
def index(skip: Optional[int] = 0, limit: Optional[int] = 100, refAgencies: RefAgenciesService = Depends()):
    return jsonable_encoder(refAgencies.list(skip,limit))

# @RefAgenciesRouter.get("/{id}")
@RefAgenciesRouter.get("/{id}", response_model=RefAgenciesSchema)
def get(id: int, refAgencies: RefAgenciesService = Depends()):
    return refAgencies.get(id)
    # return jsonable_encoder(refAgencies.get(id))

@RefAgenciesRouter.post("/", response_model=RefAgenciesSchema, status_code=status.HTTP_201_CREATED)
def create(refAgencie: RefAgenciesCreateSchema = Body(example = EXAMPLE), refAgencies: RefAgenciesService = Depends()):
    refAgencie = refAgencies.create(refAgencie)
    return refAgencie 
    # return {"name": "diatas", "infos": {} }

@RefAgenciesRouter.put("/", response_model = RefAgenciesSchema)
# @RefAgenciesRouter.put("/{id}")
def update(refAgencie: RefAgenciesUpdateSchema = Body(example = EXAMPLE1), refAgencies: RefAgenciesService = Depends()):
    return refAgencies.update(refAgencie)

@RefAgenciesRouter.delete("/{id}", response_model = RefAgenciesSchema)
# @RefAgenciesRouter.delete("/{id}")
def delete(id: int, refAgencies: RefAgenciesService = Depends()):
    return refAgencies.delete(id)

@RefAgenciesRouter.put("/restore/{id}", response_model = RefAgenciesSchema)
def restore(id: int, refAgencies: RefAgenciesService = Depends()):
    return refAgencies.retaure(id)

@RefAgenciesRouter.delete("/{id}/{signature}", response_model = RefAgenciesSchema)
def delete_signature(id: int, signature: str, refAgencies: RefAgenciesService = Depends()):
    return refAgencies.delete_signature(id, signature)

@RefAgenciesRouter.get("/items/")
def get_items(id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, refAgencies: RefAgenciesService = Depends()):
    return refAgencies.get_items(id, code, signature)






