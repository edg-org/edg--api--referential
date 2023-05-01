from pydantic import BaseModel
from typing import Union, Any, Dict, Optional
import uuid

class Coordinate(BaseModel) :
    altitude : float | None
    latitude : float | None
    longitude : float | None

class InfosSchema(BaseModel):
    name : str | None = "Region Name"
    code : str | None = "000"
    coordinate : Coordinate | None       

class RefAdmRegionsBaseSchema(BaseModel):
    # infos: Optional[Dict[str, Any]] = None
    natural_region_id: int
    infos: InfosSchema | None

class RefAdmRegionsUpdateSchema(RefAdmRegionsBaseSchema):
    id: int

class RefAdmRegionsCreateSchema(RefAdmRegionsBaseSchema):
    pass

class RefAdmRegionsSchema(RefAdmRegionsBaseSchema):
    id: int
    code : int = 100
    is_activated: Optional[bool] = True
    unique_id: Optional[str] = str(uuid.uuid1().hex)

    class Config:
        orm_mode = True

class RefAdmRegionsRtrErrorSchema(BaseModel):
	pass


class RefAdmRegionsSearchSchema(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    signature: Optional[str] = None

EXAMPLE = {
    "natural_region_id":1,
    "infos":{
        "name":"Boke",
        "code":"AR001",
        "coordinate":{
            "altitude":"000",
            "latitude":"000",
            "longitude":"000"
        }
    }
}

EXAMPLE1 = {
    "id":1,
    "natural_region_id":1,
    "infos":{
        "name":"Boke",
        "code":"AR001",
        "coordinate":{
            "altitude":"000",
            "latitude":"000",
            "longitude":"000"
        }
    }
}
