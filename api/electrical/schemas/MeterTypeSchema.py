from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class MeterModelBase(BaseModel):
    code: int
    name: str
    
    class Config:
        orm_mode = True

class CreateMeterModel(MeterModelBase):
    pass

class MeterModelSchema(MeterModelBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]