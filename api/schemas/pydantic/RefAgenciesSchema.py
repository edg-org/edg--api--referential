from pydantic import BaseModel
from typing import Union, Any, Dict, Optional
import uuid

class Coordinate(BaseModel) :
    altitude : float | None
    latitude : float | None
    longitude : float | None

class InfosSchema(BaseModel):
    name : str | None = "Agence Name"
    code : str | None = "000"
    tel : str | None = "224 600 000 000"
    email : str | None = "agence-name@edg.com.gn"
    coordinate : Coordinate | None       

class RefAgenciesBaseSchema(BaseModel):
    # infos: Optional[Dict[str, Any]] = None
    areas_id: int
    infos: InfosSchema | None

class RefAgenciesUpdateSchema(RefAgenciesBaseSchema):
    id: int

class RefAgenciesCreateSchema(RefAgenciesBaseSchema):
    pass

class RefAgenciesSchema(RefAgenciesBaseSchema):
    id: int
    is_activated: Optional[bool] = True
    unique_id: Optional[str] = str(uuid.uuid1().hex)

    class Config:
        orm_mode = True

class RefAgenciesRtrErrorSchema(BaseModel):
	pass

EXAMPLE = {
    "areas_id":0,
    "infos":{
        "name":"sandervalia",
        "code":"san001",
        "tel":"600 00 00 00",
        "email":"agence-sand@edg.com.gn",
        "coordinate":{
            "altitude":"000",
            "latitude":"000",
            "longitude":"000"
        }
    }
}

EXAMPLE1 = {
    "id":0,
    "areas_id":0,
    "infos":{
        "name":"sandervalia",
        "code":"san001",
        "tel":"600 00 00 00",
        "email":"agence-sand@edg.com.gn",
        "coordinate":{
            "altitude":"000",
            "latitude":"000",
            "longitude":"000"
        }
    }
}
