from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, Query, Body, Path, Header, Cookie, Form, File
from pydantic import Field

from api.schemas.pydantic.RefCitiesSchema import RefCitiesSchema, RefCitiesCreateSchema
from api.schemas.pydantic.RefTypeAreasSchema import (RefTypeAreasSchema, RefTypeAreasCreateSchema, EXAMPLE, 
    RefTypeAreasUpdateSchema, EXAMPLE1)

from api.services.RefTypeAreasService import RefTypeAreasService

RefTypeAreasRouter = APIRouter(prefix="/v1/typearea", tags=["Type Areas"])

@RefTypeAreasRouter.get("/", response_model = List[RefTypeAreasSchema])
def index(skip: Optional[int] = 0, limit: Optional[int] = 100, refTypeAreas: RefTypeAreasService = Depends()):
    return jsonable_encoder(refTypeAreas.list(skip,limit))

# @RefTypeAreasRouter.get("/{id}")
@RefTypeAreasRouter.get("/{id}", response_model = RefTypeAreasSchema)
def get(id: int, refTypeAreas: RefTypeAreasService = Depends()):
    return refTypeAreas.get(id)
    # return jsonable_encoder(refTypeAreas.get(id))

@RefTypeAreasRouter.post("/", response_model=RefTypeAreasSchema, status_code=status.HTTP_201_CREATED)
def create(refTypeArea: RefTypeAreasCreateSchema = Body(example = EXAMPLE), refTypeAreas: RefTypeAreasService = Depends()):
    refTypeArea = refTypeAreas.create(refTypeArea)
    return refTypeArea 

@RefTypeAreasRouter.put("/", response_model = RefTypeAreasSchema)
def update(refTypeArea: RefTypeAreasUpdateSchema = Body(example = EXAMPLE1), refTypeAreas: RefTypeAreasService = Depends()):
    return refTypeAreas.update(refTypeArea)

@RefTypeAreasRouter.delete("/{id}", response_model = RefTypeAreasSchema)
# @RefTypeAreasRouter.delete("/{id}")
def delete(id: int, refTypeAreas: RefTypeAreasService = Depends()):
    return refTypeAreas.delete(id)

@RefTypeAreasRouter.put("/restore/{id}", response_model = RefTypeAreasSchema)
def restore(id: int, refTypeAreas: RefTypeAreasService = Depends()):
    return refTypeAreas.retaure(id)

@RefTypeAreasRouter.delete("/{id}/{signature}", response_model = RefTypeAreasSchema)
def delete_signature(id: int, signature: str, refTypeAreas: RefTypeAreasService = Depends()):
    return refTypeAreas.delete_signature(id, signature)


@RefTypeAreasRouter.get("/items/")
# def get_items(id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, refTypeAreas: RefTypeAreasService = Depends()):
def get_items(id: Optional[int] = 0, signature: Optional[str] = None, refTypeAreas: RefTypeAreasService = Depends()):
    return refTypeAreas.get_items(id, "", signature)

