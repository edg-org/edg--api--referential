from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, Query, Body, Path, Header, Cookie, Form, File
from pydantic import Field

from api.schemas.pydantic.RefCitiesSchema import RefCitiesSchema, RefCitiesCreateSchema
from api.schemas.pydantic.RefCityLevelsSchema import (RefCityLevelsSchema, RefCityLevelsCreateSchema, EXAMPLE, 
    RefCityLevelsUpdateSchema, EXAMPLE1)

from api.services.RefCityLevelsService import RefCityLevelsService

RefCityLevelsRouter = APIRouter(prefix="/v1/citylevel", tags=["City Levels"])

@RefCityLevelsRouter.get("/", response_model = List[RefCityLevelsSchema])
def index(skip: Optional[int] = 0, limit: Optional[int] = 100, refCityLevels: RefCityLevelsService = Depends()):
    return jsonable_encoder(refCityLevels.list(skip,limit))

# @RefCityLevelsRouter.get("/{id}")
@RefCityLevelsRouter.get("/{id}", response_model = RefCityLevelsSchema)
def get(id: int, refCityLevels: RefCityLevelsService = Depends()):
    return refCityLevels.get(id)
    # return jsonable_encoder(refCityLevels.get(id))

@RefCityLevelsRouter.post("/", response_model=RefCityLevelsSchema, status_code=status.HTTP_201_CREATED)
def create(refCityLevel: RefCityLevelsCreateSchema = Body(example = EXAMPLE), refCityLevels: RefCityLevelsService = Depends()):
    refCityLevel = refCityLevels.create(refCityLevel)
    return refCityLevel 

@RefCityLevelsRouter.put("/", response_model = RefCityLevelsSchema)
def update(refCityLevel: RefCityLevelsUpdateSchema = Body(example = EXAMPLE1), refCityLevels: RefCityLevelsService = Depends()):
    return refCityLevels.update(refCityLevel)

@RefCityLevelsRouter.delete("/{id}", response_model = RefCityLevelsSchema)
# @RefCityLevelsRouter.delete("/{id}")
def delete(id: int, refCityLevels: RefCityLevelsService = Depends()):
    return refCityLevels.delete(id)

@RefCityLevelsRouter.put("/restore/{id}", response_model = RefCityLevelsSchema)
def restore(id: int, refCityLevels: RefCityLevelsService = Depends()):
    return refCityLevels.retaure(id)

@RefCityLevelsRouter.delete("/{id}/{signature}", response_model = RefCityLevelsSchema)
def delete_signature(id: int, signature: str, refCityLevels: RefCityLevelsService = Depends()):
    return refCityLevels.delete_signature(id, signature)

@RefCityLevelsRouter.get("/items/")
# def get_items(id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, refCityLevels: RefCityLevelsService = Depends()):
def get_items(id: Optional[int] = 0, signature: Optional[str] = None, refCityLevels: RefCityLevelsService = Depends()):
    return refCityLevels.get_items(id, "", signature)

