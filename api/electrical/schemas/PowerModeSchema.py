from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class PowerModeBase(BaseModel):
    code: int
    name: str
    
    class Config:
        orm_mode = True

class CreateMeterPoserMode(PowerModeBase):
    pass

class MeterPowerModeSchema(PowerModeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]