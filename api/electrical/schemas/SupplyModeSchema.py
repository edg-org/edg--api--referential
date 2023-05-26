from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

class SupplyModeInput(BaseModel):
    code: int
    name: str

class SupplyModeUpdate(SupplyModeInput, metaclass=HideFields):
    class Config:
        fields_hided = {'code'}

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