from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, Query, Body, Path, Header, Cookie, Form, File

from api.schemas.pydantic.RefNaturalRegionsSchema import RefNaturalRegionsSchema, RefNaturalRegionsCreateSchema
from api.schemas.pydantic.RefAdmRegionsSchema import (RefAdmRegionsSchema, RefAdmRegionsCreateSchema, EXAMPLE,
RefAdmRegionsUpdateSchema, EXAMPLE1, RefAdmRegionsSearchSchema)

from api.services.RefNaturalRegionsService import RefNaturalRegionsService
from api.services.RefAdmRegionsService import RefAdmRegionsService

RefAdmRegionsRouter = APIRouter(prefix="/v1/adminregion", tags=["Administrative Regions"])

@RefAdmRegionsRouter.get("/", response_model=List[RefAdmRegionsSchema])
def index(skip: Optional[int] = 0, limit: Optional[int] = 100, refAdmRegions: RefAdmRegionsService = Depends()):
    return jsonable_encoder(refAdmRegions.list(skip,limit))

# @RefAdmRegionsRouter.get("/{id}")
@RefAdmRegionsRouter.get("/{id}", response_model = RefAdmRegionsSchema)
def get(id: int, refAdmRegions: RefAdmRegionsService = Depends()):
    return refAdmRegions.get(id)
    # return jsonable_encoder(refAdmRegions.get(id))

@RefAdmRegionsRouter.post("/", response_model=RefAdmRegionsSchema, status_code=status.HTTP_201_CREATED)
def create(refAdmRegion: RefAdmRegionsCreateSchema = Body(example = EXAMPLE), refAdmRegions: RefAdmRegionsService = Depends()):
    refAdmRegion = refAdmRegions.create(refAdmRegion)
    return refAdmRegion 

@RefAdmRegionsRouter.put("/", response_model = RefAdmRegionsSchema)
# @RefAdmRegionsRouter.put("/{id}")
def update(refAdmRegion: RefAdmRegionsUpdateSchema = Body(example = EXAMPLE1), refAdmRegions: RefAdmRegionsService = Depends()):
    return refAdmRegions.update(refAdmRegion)

@RefAdmRegionsRouter.delete("/{id}", response_model = RefAdmRegionsSchema)
# @RefAdmRegionsRouter.delete("/{id}")
def delete(id: int, refAdmRegions: RefAdmRegionsService = Depends()):
    return refAdmRegions.delete(id)

@RefAdmRegionsRouter.put("/restore/{id}", response_model = RefAdmRegionsSchema)
def restore(id: int, refAdmRegions: RefAdmRegionsService = Depends()):
    return refAdmRegions.retaure(id)

@RefAdmRegionsRouter.delete("/{id}/{signature}", response_model = RefAdmRegionsSchema)
def delete_signature(id: int, signature: str, refAdmRegions: RefAdmRegionsService = Depends()):
    return refAdmRegions.delete_signature(id, signature)

@RefAdmRegionsRouter.get("/items/")
# @RefAdmRegionsRouter.get("/{id}", response_model = RefAdmRegionsSchema)
# def get_items(refAdmRegion: RefAdmRegionsSearchSchema, refAdmRegions: RefAdmRegionsService = Depends()):
def get_items(id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, refAdmRegions: RefAdmRegionsService = Depends()):
    return refAdmRegions.get_items(id, code, signature)
    # return refAdmRegions.get_items(refAdmRegion)
    # return jsonable_encoder(refAdmRegions.get(id))            




