from typing import Optional
from datetime import datetime
from api.configs.BaseModel import BaseSchema

#
class SupplyLineTypeSchema(BaseSchema):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateSupplyLineType(SupplyLineTypeSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class SupplyLineTypeInput(CreateSupplyLineType):
    pass

#
class SupplyLineTypeUpdate(SupplyLineTypeInput):
    pass