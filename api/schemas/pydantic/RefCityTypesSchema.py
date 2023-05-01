from pydantic import BaseModel, Field
from typing import Union, Any, Dict, Optional
from fastapi import Query, Body, Path, Header, Cookie, Form, File
import uuid

class RefCityTypesUpdateSchema(BaseModel):
    id: int
    name: str
    infos: Optional[str]

class RefCityTypesCreateSchema(BaseModel):
    name: str
    # name: str = Field(example = "Commune Urbaine")
    infos: Optional[str]

class RefCityTypesSchema(RefCityTypesCreateSchema):
    id: int
    is_activated: Optional[bool] = True
    unique_id: Optional[str] = str(uuid.uuid1().hex)

    class Config:
        orm_mode = True

class RefCityTypesRtrErrorSchema(BaseModel):
	pass


EXAMPLE = {
    "name":'Commune Urbaine',
    "infos":"Commune Urbaine type of zone"
}


EXAMPLE1 = {
    "id":0,
    "name":'Commune Urbaine',
    "infos":"Commune Urbaine type of zone"
}
