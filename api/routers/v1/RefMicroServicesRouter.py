from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, Query, Body, Path, Header, Cookie, Form, File

from api.schemas.pydantic.RefMicroServicesSchema import (RefMicroServicesSchema, RefMicroServicesCreateSchema,
RefMicroServicesUpdateSchema, EXAMPLE, EXAMPLE1)
from api.services.RefMicroServicesService import RefMicroServicesService

RefMicroServicesRouter = APIRouter(prefix="/v1/microservice", tags=["Micro Services"])

@RefMicroServicesRouter.get("/", response_model=List[RefMicroServicesSchema])
def index(skip: Optional[int] = 0, limit: Optional[int] = 100, refMicroServices: RefMicroServicesService = Depends()):
    return jsonable_encoder(refMicroServices.list(skip,limit))

# @RefMicroServicesRouter.get("/{id}")
@RefMicroServicesRouter.get("/{id}", response_model = RefMicroServicesSchema)
def get(id: int, refMicroServices: RefMicroServicesService = Depends()):
    return refMicroServices.get(id)
    # return jsonable_encoder(refMicroServices.get(id))

@RefMicroServicesRouter.post("/", response_model=RefMicroServicesSchema, status_code = status.HTTP_201_CREATED)
def create(refMicroService: RefMicroServicesCreateSchema = Body(example = EXAMPLE), refMicroServices: RefMicroServicesService = Depends()):
    refMicroService = refMicroServices.create(refMicroService)
    return refMicroService 

@RefMicroServicesRouter.put("/", response_model = RefMicroServicesSchema)
# @RefMicroServicesRouter.put("/")
def update(refMicroService: RefMicroServicesUpdateSchema = Body(example = EXAMPLE1), refMicroServices: RefMicroServicesService = Depends()):
    return refMicroServices.update(refMicroService)

@RefMicroServicesRouter.delete("/{id}", response_model = RefMicroServicesSchema)
# @RefMicroServicesRouter.delete("/{id}")
def delete(id: int, refMicroServices: RefMicroServicesService = Depends()):
    return refMicroServices.delete(id)

@RefMicroServicesRouter.put("/restore/{id}", response_model = RefMicroServicesSchema)
# @RefMicroServicesRouter.put("/restore/{id}")
def restore(id: int, refMicroServices: RefMicroServicesService = Depends()):
    return refMicroServices.retaure(id)

# @RefMicroServicesRouter.delete("/{id}/{signature}")
@RefMicroServicesRouter.delete("/{id}/{signature}", response_model = RefMicroServicesSchema)
def delete_signature(id: int, signature: str, refMicroServices: RefMicroServicesService = Depends()):
    return refMicroServices.delete_signature(id, signature)

@RefMicroServicesRouter.get("/items/")
def get_items(id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, refMicroServices: RefMicroServicesService = Depends()):
    return refMicroServices.get_items(id, code, signature)

