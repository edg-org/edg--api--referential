from datetime import datetime
from typing import List, Any, Dict
from api.configs.BaseModel import BaseSchema

class InfosSchema(BaseSchema):
    microservice_name: str
    endpoint: str
    verb: str
    user_email: str
    previous_metadata: Dict[str, Any]
    current_metadata: Dict[str, Any]
    
class LogSchema(BaseSchema):
    id: int
    created_at: datetime
    infos: InfosSchema
    
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

#
class LogPagination(BaseSchema):
    count: int
    total: int
    page_size: int
    start_index: int
    results: List[LogSchema] = []