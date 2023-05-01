from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, Query, Body, Path, Header, Cookie, Form, File
from pydantic import Field

from api.schemas.pydantic.RefCitiesSchema import RefCitiesSchema, RefCitiesCreateSchema
from api.schemas.pydantic.RefCityTypesSchema import (RefCityTypesSchema, RefCityTypesCreateSchema, EXAMPLE, RefCityTypesUpdateSchema, EXAMPLE1)

from api.services.RefCityTypesService import RefCityTypesService

RefCityTypesRouter = APIRouter(prefix="/v1/citytype", tags=["City Types"])

@RefCityTypesRouter.get("/", response_model = List[RefCityTypesSchema])
def index(skip: Optional[int] = 0, limit: Optional[int] = 100, refCityTypes: RefCityTypesService = Depends()):
    return jsonable_encoder(refCityTypes.list(skip,limit))

# @RefCityTypesRouter.get("/{id}")
@RefCityTypesRouter.get("/{id}", response_model = RefCityTypesSchema)
def get(id: int, refCityTypes: RefCityTypesService = Depends()):
    return refCityTypes.get(id)
    # return jsonable_encoder(refCityTypes.get(id))

@RefCityTypesRouter.post("/", response_model = RefCityTypesSchema, status_code = status.HTTP_201_CREATED)
def create(refCityType: RefCityTypesCreateSchema = Body(example = EXAMPLE), refCityTypes: RefCityTypesService = Depends()):
    refCityType = refCityTypes.create(refCityType)
    return refCityType 

@RefCityTypesRouter.put("/", response_model = RefCityTypesSchema)
def update(refCityType: RefCityTypesUpdateSchema = Body(example = EXAMPLE1), refCityTypes: RefCityTypesService = Depends()):
    return refCityTypes.update(refCityType)

@RefCityTypesRouter.delete("/{id}", response_model = RefCityTypesSchema)
# @RefCityTypesRouter.delete("/{id}")
def delete(id: int, refCityTypes: RefCityTypesService = Depends()):
    return refCityTypes.delete(id)

@RefCityTypesRouter.put("/restore/{id}", response_model = RefCityTypesSchema)
def restore(id: int, refCityTypes: RefCityTypesService = Depends()):
    return refCityTypes.retaure(id)

@RefCityTypesRouter.delete("/{id}/{signature}", response_model = RefCityTypesSchema)
def delete_signature(id: int, signature: str, refCityTypes: RefCityTypesService = Depends()):
    return refCityTypes.delete_signature(id, signature)

@RefCityTypesRouter.get("/items/")
# def get_items(id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, refCityTypes: RefCityTypesService = Depends()):
def get_items(id: Optional[int] = 0, signature: Optional[str] = None, refCityTypes: RefCityTypesService = Depends()):
    return refCityTypes.get_items(id, "", signature)

