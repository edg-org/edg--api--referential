from pydantic import BaseModel
from typing import Union, Any, Dict, Optional, List
import uuid

class Coordinate(BaseModel) :
    altitude : float | None
    latitude : float | None
    longitude : float | None

class InfosSchema(BaseModel):
    name : str | None = "name"
    code : str | None = "0000"
    coordinate : Coordinate | None       

class RefRegionalDelegationsBaseSchema(BaseModel):
    # infos: Optional[Dict[str, Any]] = None
    infos : InfosSchema | None

class RefRegionalDelegationsUpdateSchema(RefRegionalDelegationsBaseSchema):
    id: int

class RefRegionalDelegationsCreateSchema(RefRegionalDelegationsBaseSchema):
    pass
 
class RefRegionalDelegationsSchema(RefRegionalDelegationsBaseSchema):
    id: int
    code : int = 10
    is_activated: Optional[bool] = True
    unique_id: Optional[str] = str(uuid.uuid1().hex)

    class Config:
        orm_mode = True

class RefRegionalDelegationsRtrErrorSchema(BaseModel):
	pass 

class RefRegionalDelegationsSearchSchema(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    signature: Optional[str] = None


EXAMPLE = {
    "infos":{ 
        "name":"DR Conakry",
        "code":"01",
        "coordinate":{
            "altitude":"000",
            "latitude":"000",
            "longitude":"000"
        }
    }
}
EXAMPLE1 = {
    "id":10,
    "infos":{
        "name":"DR Kankan",
        "code":"01",
        "coordinate":{
            "altitude":"000",
            "latitude":"000",
            "longitude":"000"
        }
    }
}
