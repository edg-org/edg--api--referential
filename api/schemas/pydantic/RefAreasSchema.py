from pydantic import BaseModel
from typing import Union, Any, Dict, Optional
from fastapi import APIRouter, Depends, status, Query, Body, Path, Header, Cookie, Form, File
import uuid

class Coordinate(BaseModel) :
    altitude : float | None
    latitude : float | None
    longitude : float | None

class InfosSchema(BaseModel):
    name : str | None = "Area Name"
    code : str | None = "000"
    coordinate : Coordinate | None       

class RefAreasBaseSchema(BaseModel):
    cities_id: int
    type_areas_id: int
    infos: InfosSchema | None

class RefAreasUpdateSchema(RefAreasBaseSchema):
    id: int
    # cities_id: int
    # type_areas_id: int
    # infos: Optional[Dict[str, Any]] = None

class RefAreasCreateSchema(RefAreasBaseSchema):   
    pass

class RefAreasSchema(RefAreasCreateSchema):
    id: int
    code : int = 1000000
    is_activated: Optional[bool] = True
    unique_id: Optional[str] = str(uuid.uuid1().hex)

    class Config:
        orm_mode = True

class RefAreasRtrErrorSchema(BaseModel):
	pass

EXAMPLE = {
    "cities_id":1,
    "type_areas_id":1,
    "infos":{
        "name":"Sangoyah",
        "code":"SAN001",
        "coordinate":{
            "altitude":"000",
            "latitude":"000",
            "longitude":"000"
        }
    }
}

EXAMPLE1 = {
    "id":1,
    "cities_id":1,
    "type_areas_id":1,
    "infos":{
        "name":"Sangoyah",
        "code":"SAN001",
        "coordinate":{
            "altitude":"000",
            "latitude":"000",
            "longitude":"000"
        }
    }
}
