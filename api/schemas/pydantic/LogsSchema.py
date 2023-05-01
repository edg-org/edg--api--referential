from pydantic import BaseModel
from typing import Union, Any, Dict, Optional
import uuid

class InfosSchema(BaseModel):
    microservice: Optional[str] = None
    endpoint: Optional[str] = None
    user_uid: Optional[str] = None
    user_email: Optional[str] = None
    verb: Optional[str] = None
    user: Optional[Dict[str, Any]] = None
    prev_data: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    micro_service_uid: Optional[str] = None

class LogsBaseSchema(BaseModel):
    micro_service_uid: Optional[str] = str(uuid.uuid1().hex)
    infos: InfosSchema | None

# class LogsBaseSchema(BaseModel):
#     # microservice: Optional[str] = None
#     # endpoint: Optional[str] = None
#     # user_uid: Optional[str] = None
#     # user_email: Optional[str] = None
#     # verb: Optional[str] = None
#     # user: Optional[Dict[str, Any]] = None
#     # prev_data: Optional[Dict[str, Any]] = None
#     # data: Optional[Dict[str, Any]] = None
#     micro_service_uid: Optional[str] = None
#     infos: Optional[Dict[str, Any]] = None

class LogsUpdateSchema(LogsBaseSchema):
    id: int

class LogsCreateSchema(LogsBaseSchema):
    pass

class LogsSchema(LogsBaseSchema):
    id: int
    is_activated: Optional[bool] = True
    unique_id: Optional[str] = str(uuid.uuid1().hex)

    class Config:
        orm_mode = True

class LogsRtrErrorSchema(BaseModel):
    pass

EXAMPLE = {
    "infos":{
        "microservice":"contact & subscription",
        "endpoint":"/contact/",
        "user_uid":"e5cc6c82da3a11eda3bbdf1178d790b2", # a supprimé                 
        "user_email":"oussou.diakite@gmail.com",                                       
        "verb":"get",
        "user":{"name":"diatas","email":"diatas2@gmail.com","phone":"224625356176"},   #  a supprimé 
        "prev_data":{"name":"devinfo","email":"devinfo@gmail.com","phone":"224625356176"},  #_previous_metadata
        "data":{"name":"diatas","email":"diatas2@gmail.com","phone":"224625356176"}   # _metadata
    }
}

EXAMPLE1 = {
    "id":1,
    "infos":{
        "microservice":"contact & subscription",
        "endpoint":"/contact/",
        "user_uid":"e5cc6c82da3a11eda3bbdf1178d790b2",
        "user_email":"oussou.diakite@gmail.com",
        "verb":"get",
        "user":{"name":"diatas","email":"diatas2@gmail.com","phone":"224625356176"},    
        "prev_data":{"name":"devinfo","email":"devinfo@gmail.com","phone":"224625356176"},    
        "data":{"name":"diatas","email":"diatas2@gmail.com","phone":"224625356176"}   
    }
}
