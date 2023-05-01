from pydantic import BaseModel
from typing import Union, Any, Dict, Optional, List
import uuid

class Coordinate(BaseModel) :
    phone : str | None = "224 600 000 000"
    email : str | None = "agence-name@edg.com.gn"
    github : str | None = "https://github.com/diatas"

class InfosSchema(BaseModel):
    name : str | None = "Referenciel Geographique"
    code : str | None = "000"
    coordinate : List[Coordinate] | None       

class RefMicroServicesBaseSchema(BaseModel):
    # infos: Optional[Dict[str, Any]] = None
    infos: InfosSchema | None

class RefMicroServicesUpdateSchema(RefMicroServicesBaseSchema):
    id: int

class RefMicroServicesCreateSchema(RefMicroServicesBaseSchema):
    pass
 
class RefMicroServicesSchema(RefMicroServicesBaseSchema):
    id: int
    is_activated: Optional[bool] = True
    unique_id: Optional[str] = str(uuid.uuid1().hex)

    class Config:
        orm_mode = True

class RefMicroServicesRtrErrorSchema(BaseModel):
	pass 

class RefMicroServicesSearchSchema(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    signature: Optional[str] = None

EXAMPLE = {
    "infos":{
        "name":"Referenciel Geographique",
        "code":"01",
        "coordinate":[{
            "phone":"224 600 000 000",
            "email":"agence-name@edg.com.gn",
            "github":"https://github.com/diatas"
        },]
    }
}

EXAMPLE1 = {
    "id":1,
    "infos":{
        "name":"Referenciel Electrique",
        "code":"01",
        "coordinate":[{
            "phone":"224 600 000 000",
            "email":"agence-name@edg.com.gn",
            "github":"https://github.com/diatas"
        },]
    }
}
