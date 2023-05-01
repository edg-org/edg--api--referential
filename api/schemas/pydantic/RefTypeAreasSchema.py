from pydantic import BaseModel, Field
from typing import Union, Any, Dict, Optional
from fastapi import Query, Body, Path, Header, Cookie, Form, File
import uuid

class RefTypeAreasUpdateSchema(BaseModel):
    id: int
    name: str
    infos: Optional[str]

class RefTypeAreasCreateSchema(BaseModel):
    name: str
    # name: str = Field(example = "Quartier")
    infos: Optional[str]

    # class Config:
    #     schema_extra = {
    #         "example":{

    #             "name":"Quartier",
    #             "infos":"le type de zone quartier",

    #         }

    #     }

            

class RefTypeAreasSchema(RefTypeAreasCreateSchema):
    id: int
    is_activated: Optional[bool] = True
    unique_id: Optional[str] = str(uuid.uuid1().hex)

    class Config:
        orm_mode = True

class RefTypeAreasRtrErrorSchema(BaseModel):
	pass


EXAMPLE = {
    "name":'quartier',
    "infos":"arrea type of zone"
}


EXAMPLE1 = {
    "id":0,
    "name":'quartier',
    "infos":"arrea type of zone"
}
