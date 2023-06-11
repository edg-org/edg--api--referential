from typing import Optional
from datetime import datetime
from api.configs.BaseModel import BaseSchema

#
class ContactTypeSchema(BaseSchema):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateContactType(ContactTypeSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class ContactTypeInput(CreateContactType):
    pass

#
class ContactTypeUpdate(ContactTypeInput):
    class Config:
        fields_to_hide = {"code"}