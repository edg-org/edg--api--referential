from typing import Any, Dict
from datetime import datetime
from pydantic import BaseModel

class InfosSchema(BaseModel):
    microservice_name: str
    endpoint: str
    verb: str
    user_email: str
    previous_metadata: Dict[str, Any]
    current_metadata: Dict[str, Any]

class LoggerBase(BaseModel):
    infos: InfosSchema

    class Config:
        orm_mode = True
class CreateLogger(LoggerBase):
    pass

class LoggerSchema(LoggerBase):
    id: int
    created_at: datetime