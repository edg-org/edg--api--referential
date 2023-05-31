from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

#
class ContactTypeSchema(BaseModel):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateContactType(ContactTypeSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class ContactTypeInput(CreateContactType, metaclass=HideFields):
    class Config:
        fields_hided = {"code"}

#
class ContactTypeUpdate(ContactTypeInput):
    pass