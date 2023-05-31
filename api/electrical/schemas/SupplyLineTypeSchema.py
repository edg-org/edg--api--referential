from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

#
class SupplyLineTypeSchema(BaseModel):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateSupplyLineType(SupplyLineTypeSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class SupplyLineTypeInput(CreateSupplyLineType, metaclass=HideFields):
    class Config:
        fields_hided = {"code"}

#
class SupplyLineTypeUpdate(SupplyLineTypeInput):
    pass