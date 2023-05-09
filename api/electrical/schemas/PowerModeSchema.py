from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class PowerModeUpdate(BaseModel):
    name: str

class PowerModeInput(PowerModeUpdate):
    code: int

class PowerModeBase(PowerModeInput):
    pass

    class Config:
        orm_mode = True

class CreatePowerMode(PowerModeBase):
    pass

class PowerModeSchema(PowerModeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]