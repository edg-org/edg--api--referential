from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, Query, Body, Path, Header, Cookie, Form, File
from api.schemas.pydantic.RefCitiesSchema import RefCitiesSchema, RefCitiesCreateSchema
from api.schemas.pydantic.RefAreasSchema import RefAreasSchema, RefAreasCreateSchema, EXAMPLE, RefAreasUpdateSchema, EXAMPLE1

from api.services.RefCitiesService import RefCitiesService
from api.services.RefAreasService import RefAreasService

RefAreasRouter = APIRouter(prefix="/v1/area", tags=["Areas"])

@RefAreasRouter.get("/", response_model=List[RefAreasSchema])
def index(skip: Optional[int] = 0, limit: Optional[int] = 100, refAreas: RefAreasService = Depends()):
    return jsonable_encoder(refAreas.list(skip,limit))
  
# @RefAreasRouter.get("/{id}")
@RefAreasRouter.get("/{id}", response_model = RefAreasSchema)
def get(id: int, refAreas: RefAreasService = Depends()):
    return refAreas.get(id)
    # return jsonable_encoder(refAreas.get(id))

@RefAreasRouter.post("/", response_model=RefAreasSchema, status_code=status.HTTP_201_CREATED)
def create(refArea: RefAreasCreateSchema = Body(example = EXAMPLE), refAreas: RefAreasService = Depends()):
    refArea = refAreas.create(refArea)
    return refArea 
    # return {"name": "diatas", "infos": {} }

@RefAreasRouter.put("/", response_model = RefAreasSchema)
# @RefAreasRouter.put("/{id}")
def update(refArea: RefAreasUpdateSchema = Body(example = EXAMPLE1), refAreas: RefAreasService = Depends()):
    return refAreas.update(refArea)

@RefAreasRouter.delete("/{id}", response_model = RefAreasSchema)
# @RefAreasRouter.delete("/{id}")
def delete(id: int, refAreas: RefAreasService = Depends()):
    return refAreas.delete(id)

@RefAreasRouter.put("/restore/{id}", response_model = RefAreasSchema)
def restore(id: int, refAreas: RefAreasService = Depends()):
    return refAreas.retaure(id)

@RefAreasRouter.delete("/{id}/{signature}", response_model = RefAreasSchema)
def delete_signature(id: int, signature: str, refAreas: RefAreasService = Depends()):
    return refAreas.delete_signature(id, signature)

@RefAreasRouter.get("/items/")
def get_items(id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, refAreas: RefAreasService = Depends()):
    return refAreas.get_items(id, code, signature)

