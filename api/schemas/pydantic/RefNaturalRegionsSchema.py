from pydantic import BaseModel
from typing import Union, Any, Dict, Optional, List
from api.models.RefAdmRegionsModel import RefAdmRegions
import uuid

class Coordinate(BaseModel) :
    altitude : float | None
    latitude : float | None
    longitude : float | None

class InfosSchema(BaseModel):
    name : str | None = "Natural Name"
    code : str | None = "000"
    coordinate : Coordinate | None       

class RefNaturalRegionsBaseSchema(BaseModel):
    # infos: Optional[Dict[str, Any]] = None
    infos: InfosSchema | None

class RefNaturalRegionsUpdateSchema(RefNaturalRegionsBaseSchema):
    id: int

class RefNaturalRegionsCreateSchema(RefNaturalRegionsBaseSchema):
    pass
    # name: str
    # infos: Optional[Dict[str, Any]] = None
    # infos: Dict[str, Any]
    # infos : Union[dict, None] = None

    # def infos_to_json(self):
    # 	# json.dumps(myDict)
    # 	return {
    # 		'name':
    # 	}

class RefNaturalRegionsSchema(RefNaturalRegionsBaseSchema):
    id: int
    code : int = 10
    is_activated: Optional[bool] = True
    unique_id: Optional[str] = str(uuid.uuid1().hex)

    class Config:
        orm_mode = True

class RefNaturalRegionsRtrErrorSchema(BaseModel):
	pass
 

class RefNaturalRegionsSearchSchema(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    signature: Optional[str] = None

# class RefNaturalRegionsRSReadSchema(RefNaturalRegionsSchema):
#     adm_regions: Optional[List[RefAdmRegions]] 

EXAMPLE = {
    "infos":{
        "name":"Basse Guinee",
        "code":"NR001",
        "coordinate":{
            "altitude":"000",
            "latitude":"000",
            "longitude":"000"
        }
    }
}
EXAMPLE1 = {
    "id":0,
    "infos":{
        "name":"Haute Guinee",
        "code":"NR001",
        "coordinate":{
            "altitude":"000",
            "latitude":"000",
            "longitude":"000"
        }
    }
}
