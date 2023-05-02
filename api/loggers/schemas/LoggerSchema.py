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

class LoggerBaseSchema(BaseModel):
    infos: InfosSchema

class LogsUpdateSchema(LoggerBaseSchema):
    id: int

class LoggerCreateSchema(LoggerBaseSchema):
    pass

class LoggerSchema(LoggerBaseSchema):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class LoggerRtrErrorSchema(BaseModel):
    pass
