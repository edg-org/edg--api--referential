from typing import Any, Dict
from datetime import datetime
from api.configs.BaseModel import BaseSchema
from typing import Optional
class InfosSchema(BaseSchema):
    microservice_name: Optional[str]
    endpoint: Optional[str]
    verb: Optional[str]
    user_email: Optional[str]
    previous_metadata: Optional[Dict[str, Any]]
    current_metadata: Optional[Dict[str, Any]]
    
class LogSchema(BaseSchema):
    id: Optional[int]
    created_at: Optional[datetime]
    infos: Optional[InfosSchema]
    
    class Config:
        orm_mode = True

class CreateLog(LogSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at"
        }

class LogInput(CreateLog):
    pass