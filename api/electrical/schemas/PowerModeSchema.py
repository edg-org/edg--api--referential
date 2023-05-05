from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class PowerModeBase(BaseModel):
    code: int
    name: str

    class Config:
        orm_mode = True


class CreatePowerMode(PowerModeBase):
    pass


class PowerModeSchema(PowerModeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
