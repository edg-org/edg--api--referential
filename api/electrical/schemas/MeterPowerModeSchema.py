from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class MeterPowerModeBase(BaseModel):
    code: int
    name: str
    
    class Config:
        orm_mode = True

class CreateMeterPoserMode(MeterPowerModeBase):
    pass

class MeterPowerModeSchema(MeterPowerModeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]