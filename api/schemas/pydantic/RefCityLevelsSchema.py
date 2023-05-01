from pydantic import BaseModel, Field
from typing import Union, Any, Dict, Optional
from fastapi import Query, Body, Path, Header, Cookie, Form, File
import uuid

class RefCityLevelsUpdateSchema(BaseModel):
    id: int
    name: str
    infos: Optional[str]

class RefCityLevelsCreateSchema(BaseModel):
    name: str
    # name: str = Field(example = "Préfecture")
    infos: Optional[str]

class RefCityLevelsSchema(RefCityLevelsCreateSchema):
    id: int
    is_activated: Optional[bool] = True
    unique_id: Optional[str] = str(uuid.uuid1().hex)

    class Config:
        orm_mode = True

class RefCityLevelsRtrErrorSchema(BaseModel):
	pass


EXAMPLE = {
    "name":'Préfecture',
    "infos":"arrea type of zone"
}


EXAMPLE1 = {
    "id":0,
    "name":'Préfecture',
    "infos":"arrea type of zone"
}
