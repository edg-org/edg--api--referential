from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

#
class SupplyModeSchema(BaseModel):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateSupplyMode(SupplyModeSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class SupplyModeInput(CreateSupplyMode, metaclass=HideFields):
    class Config:
        fields_hided = {"code"}

#
class SupplyModeUpdate(SupplyModeInput):
    pass