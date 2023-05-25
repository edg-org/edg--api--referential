from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import OmitFields

class SupplyLineTypeInput(BaseModel):
    code: int
    name: str

class SupplyLineTypeUpdate(SupplyLineTypeInput, metaclass=OmitFields):
    class Config:
        omit_fields = {'code'}

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