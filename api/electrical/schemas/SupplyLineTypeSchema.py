from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class SupplyLineTypeUpdate(BaseModel):
    name: str

class SupplyLineTypeInput(SupplyLineTypeUpdate):
    code: int

class SupplyLineTypeBase(SupplyLineTypeInput):
    pass

    class Config:
        orm_mode = True

class CreateSupplyLineType(SupplyLineTypeBase):
    pass

class SupplyLineTypeSchema(SupplyLineTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]