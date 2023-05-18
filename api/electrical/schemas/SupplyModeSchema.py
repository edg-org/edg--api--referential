from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class SupplyModeUpdate(BaseModel):
    name: str

class SupplyModeInput(SupplyModeUpdate):
    code: int

class SupplyModeBase(SupplyModeInput):
    pass

    class Config:
        orm_mode = True

class CreateSupplyMode(SupplyModeBase):
    pass

class SupplyModeSchema(SupplyModeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]