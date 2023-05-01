from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, Query, Body, Path, Header, Cookie, Form, File

from api.schemas.pydantic.RefNaturalRegionsSchema import (RefNaturalRegionsSchema, RefNaturalRegionsCreateSchema,
RefNaturalRegionsUpdateSchema, EXAMPLE, EXAMPLE1)
from api.services.RefNaturalRegionsService import RefNaturalRegionsService

RefNaturalRegionsRouter = APIRouter(prefix="/v1/naturalregion", tags=["Natural Regions"])

@RefNaturalRegionsRouter.get("/", response_model=List[RefNaturalRegionsSchema])
def index(skip: Optional[int] = 0, limit: Optional[int] = 100, refNaturalRegions: RefNaturalRegionsService = Depends()):
    return jsonable_encoder(refNaturalRegions.list(skip,limit))

# @RefNaturalRegionsRouter.get("/{id}")
@RefNaturalRegionsRouter.get("/{id}", response_model = RefNaturalRegionsSchema)
def get(id: int, refNaturalRegions: RefNaturalRegionsService = Depends()):
    return refNaturalRegions.get(id)
    # return jsonable_encoder(refNaturalRegions.get(id))

@RefNaturalRegionsRouter.post("/", response_model=RefNaturalRegionsSchema, status_code = status.HTTP_201_CREATED)
def create(refNaturalRegion: RefNaturalRegionsCreateSchema = Body(example = EXAMPLE), refNaturalRegions: RefNaturalRegionsService = Depends()):
    refNaturalRegion = refNaturalRegions.create(refNaturalRegion)
    return refNaturalRegion 

@RefNaturalRegionsRouter.put("/", response_model = RefNaturalRegionsSchema)
# @RefNaturalRegionsRouter.put("/")
def update(refNaturalRegion: RefNaturalRegionsUpdateSchema = Body(example = EXAMPLE1), refNaturalRegions: RefNaturalRegionsService = Depends()):
    return refNaturalRegions.update(refNaturalRegion)

@RefNaturalRegionsRouter.delete("/{id}", response_model = RefNaturalRegionsSchema)
# @RefNaturalRegionsRouter.delete("/{id}")
def delete(id: int, refNaturalRegions: RefNaturalRegionsService = Depends()):
    return refNaturalRegions.delete(id)

@RefNaturalRegionsRouter.put("/restore/{id}", response_model = RefNaturalRegionsSchema)
# @RefNaturalRegionsRouter.put("/restore/{id}")
def restore(id: int, refNaturalRegions: RefNaturalRegionsService = Depends()):
    return refNaturalRegions.retaure(id)

# @RefNaturalRegionsRouter.delete("/{id}/{signature}")
@RefNaturalRegionsRouter.delete("/{id}/{signature}", response_model = RefNaturalRegionsSchema)
def delete_signature(id: int, signature: str, refNaturalRegions: RefNaturalRegionsService = Depends()):
    return refNaturalRegions.delete_signature(id, signature)


@RefNaturalRegionsRouter.get("/items/")
def get_items(id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, refNaturalRegions: RefNaturalRegionsService = Depends()):
    return refNaturalRegions.get_items(id, code, signature)

