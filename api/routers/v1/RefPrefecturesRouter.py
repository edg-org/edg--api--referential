from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, Query, Body, Path, Header, Cookie, Form, File

from api.schemas.pydantic.RefNaturalRegionsSchema import RefNaturalRegionsSchema, RefNaturalRegionsCreateSchema
from api.schemas.pydantic.RefPrefecturesSchema import (RefPrefecturesSchema, RefPrefecturesCreateSchema, EXAMPLE,
RefPrefecturesUpdateSchema, EXAMPLE1)

from api.services.RefNaturalRegionsService import RefNaturalRegionsService
from api.services.RefPrefecturesService import RefPrefecturesService

RefPrefecturesRouter = APIRouter(prefix="/v1/prefecture", tags=["Prefectures"])

@RefPrefecturesRouter.get("/", response_model=List[RefPrefecturesSchema])
def index(skip: Optional[int] = 0, limit: Optional[int] = 100, refPrefectures: RefPrefecturesService = Depends()):
    return jsonable_encoder(refPrefectures.list(skip,limit))

# @RefPrefecturesRouter.get("/{id}")
@RefPrefecturesRouter.get("/{id}", response_model = RefPrefecturesSchema) 
def get(id: int, refPrefectures: RefPrefecturesService = Depends()):
    return refPrefectures.get(id)
    # return jsonable_encoder(refPrefectures.get(id))


@RefPrefecturesRouter.post("/", response_model=RefPrefecturesSchema, status_code=status.HTTP_201_CREATED)
def create(refPrefecture: RefPrefecturesCreateSchema = Body(example = EXAMPLE), refPrefectures: RefPrefecturesService = Depends()):
    refPrefecture = refPrefectures.create(refPrefecture)
    return refPrefecture 

@RefPrefecturesRouter.put("/", response_model = RefPrefecturesSchema)
# @RefPrefecturesRouter.put("/{id}")
def update(refPrefecture: RefPrefecturesUpdateSchema = Body(example = EXAMPLE1), refPrefectures: RefPrefecturesService = Depends()):
    return refPrefectures.update(refPrefecture)

@RefPrefecturesRouter.delete("/{id}", response_model = RefPrefecturesSchema)
# @RefPrefecturesRouter.delete("/{id}")
def delete(id: int, refPrefectures: RefPrefecturesService = Depends()):
    return refPrefectures.delete(id)

@RefPrefecturesRouter.put("/restore/{id}", response_model = RefPrefecturesSchema)
def restore(id: int, refPrefectures: RefPrefecturesService = Depends()):
    return refPrefectures.retaure(id)

@RefPrefecturesRouter.delete("/{id}/{signature}", response_model = RefPrefecturesSchema)
def delete_signature(id: int, signature: str, refPrefectures: RefPrefecturesService = Depends()):
    return refPrefectures.delete_signature(id, signature)


@RefPrefecturesRouter.get("/items/")
def get_items(id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, refPrefectures: RefPrefecturesService = Depends()):
    return refPrefectures.get_items(id, code, signature)

