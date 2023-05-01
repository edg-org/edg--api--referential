from pydantic import BaseModel
from typing import Union, Any, Dict, Optional
import uuid

class Coordinate(BaseModel) :
    altitude : float | None
    latitude : float | None
    longitude : float | None

class InfosSchema(BaseModel):
    name : str | None
    code : str | None
    coordinate : Coordinate | None       

class RefCitiesBaseSchema(BaseModel):
    prefecture_id: int
    type_id: int
    level_id: int
    # infos: Optional[Dict[str, Any]] = None
    infos: InfosSchema | None

class RefCitiesUpdateSchema(RefCitiesBaseSchema):
    id: int


class RefCitiesCreateSchema(RefCitiesBaseSchema):
    pass


class RefCitiesSchema(RefCitiesCreateSchema):
    id: int
    code : int = 1000
    is_activated: Optional[bool] = True
    unique_id: Optional[str] = str(uuid.uuid1().hex)

    class Config:
        orm_mode = True

class RefCitiesRtrErrorSchema(BaseModel):
	pass

EXAMPLE = {
    "prefecture_id":1,
    "type_id":1,
    "level_id":1,
    "infos":{
        "name":"Matoto",
        "code":"CI001",
        "coordinate":{
            "altitude":"000",
            "latitude":"000",
            "longitude":"000"
        }
    }
}

EXAMPLE1 = {
    "id":1,
    "prefecture_id":1,
    "type_id":1,
    "level_id":1,
    "infos":{
        "name":"Matoto",
        "code":"CI001",
        "coordinate":{
            "altitude":"000",
            "latitude":"000",
            "longitude":"000"
        }
    }
}
