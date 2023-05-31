from typing import Any, Dict
from datetime import datetime
from api.configs.BaseModel import SchemaModel

class InfosSchema(SchemaModel):
    microservice_name: str
    endpoint: str
    verb: str
    user_email: str
    previous_metadata: Dict[str, Any]
    current_metadata: Dict[str, Any]
    
class LoggerSchema(SchemaModel):
    id: int
    created_at: datetime
    infos: InfosSchema
    
    class Config:
        orm_mode = True

class CreateLogger(LoggerSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at"
        }

class LoggerInput(CreateLogger):
    pass