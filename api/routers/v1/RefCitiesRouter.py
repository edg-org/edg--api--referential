from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, Query, Body, Path, Header, Cookie, Form, File

from api.schemas.pydantic.RefNaturalRegionsSchema import RefNaturalRegionsSchema, RefNaturalRegionsCreateSchema
from api.schemas.pydantic.RefPrefecturesSchema import RefPrefecturesSchema, RefPrefecturesCreateSchema
from api.schemas.pydantic.RefCitiesSchema import (RefCitiesSchema, RefCitiesCreateSchema, EXAMPLE,RefCitiesUpdateSchema,
EXAMPLE1)

from api.services.RefNaturalRegionsService import RefNaturalRegionsService
from api.services.RefPrefecturesService import RefPrefecturesService
from api.services.RefCitiesService import RefCitiesService

RefCitiesRouter = APIRouter(prefix="/v1/city", tags=["Cities"])

@RefCitiesRouter.get("/", response_model=List[RefCitiesSchema])
def index(skip: Optional[int] = 0, limit: Optional[int] = 100, refCities: RefCitiesService = Depends()):
    return jsonable_encoder(refCities.list(skip,limit))

# @RefCitiesRouter.get("/{id}")
@RefCitiesRouter.get("/{id}", response_model=RefCitiesSchema)
def get(id: int, refCities: RefCitiesService = Depends()):
    return refCities.get(id)
    # return jsonable_encoder(refCities.get(id))

@RefCitiesRouter.post("/", response_model=RefCitiesSchema, status_code=status.HTTP_201_CREATED)
def create(refCitie: RefCitiesCreateSchema = Body(example = EXAMPLE), refCities: RefCitiesService = Depends()):
    refCitie = refCities.create(refCitie)
    return refCitie 

@RefCitiesRouter.put("/", response_model = RefCitiesSchema)
# @RefCitiesRouter.put("/{id}")
def update(refCitie: RefCitiesUpdateSchema = Body(example = EXAMPLE1), refCities: RefCitiesService = Depends()):
    return refCities.update(refCitie)

@RefCitiesRouter.delete("/{id}", response_model = RefCitiesSchema) 
# @RefCitiesRouter.delete("/{id}")
def delete(id: int, refCities: RefCitiesService = Depends()):
    return refCities.delete(id)

@RefCitiesRouter.put("/restore/{id}", response_model = RefCitiesSchema)
def restore(id: int, refCities: RefCitiesService = Depends()):
    return refCities.retaure(id)

@RefCitiesRouter.delete("/{id}/{signature}", response_model = RefCitiesSchema)
def delete_signature(id: int, signature: str, refCities: RefCitiesService = Depends()):
    return refCities.delete_signature(id, signature)

# @RefCitiesRouter.get("/code/{code}", response_model = RefCitiesSchema)
# def get_code(code: str, refCities: RefCitiesService = Depends()):
#     return refCities.get_code(code)

@RefCitiesRouter.get("/items/")
def get_items(id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, refCities: RefCitiesService = Depends()):
    return refCities.get_items(id, code, signature)





