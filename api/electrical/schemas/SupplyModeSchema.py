from typing import Optional
from datetime import datetime
from api.configs.BaseModel import BaseSchema

#
class SupplyModeSchema(BaseSchema):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateSupplyMode(SupplyModeSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class SupplyModeInput(CreateSupplyMode):
    class Config:
        fields_to_hide = {"code"}

#
class SupplyModeUpdate(SupplyModeInput):
    pass