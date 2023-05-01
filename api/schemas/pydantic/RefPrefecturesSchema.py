from pydantic import BaseModel
from typing import Union, Any, Dict, Optional
import uuid

class Coordinate(BaseModel) :
    altitude : float | None
    latitude : float | None
    longitude : float | None

class InfosSchema(BaseModel):
    name : str | None = "Prefecture Name"
    code : str | None = "000"
    coordinate : Coordinate | None       

class RefPrefecturesBaseSchema(BaseModel):
    # infos: Optional[Dict[str, Any]] = None
    region_id: int
    infos: InfosSchema | None

class RefPrefecturesUpdateSchema(RefPrefecturesBaseSchema):
    id: int

class RefPrefecturesCreateSchema(RefPrefecturesBaseSchema):
    pass

class RefPrefecturesSchema(RefPrefecturesCreateSchema):
    id: int
    code : int = 1000
    is_activated: Optional[bool] = True
    unique_id: Optional[str] = str(uuid.uuid1().hex)

    class Config:
        orm_mode = True

class RefPrefecturesRtrErrorSchema(RefPrefecturesBaseSchema):
	pass


EXAMPLE = {
    "region_id":1,
    "infos":{
        "name":"Kolaboui",
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
    "region_id":1,
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


