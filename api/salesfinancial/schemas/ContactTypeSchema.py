from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import OmitFields

class ContactTypeInput(BaseModel):
    code: int
    name: str

class ContactTypeUpdate(ContactTypeInput, metaclass=OmitFields):
    class Config:
        omit_fields = {'code'}

class ContactTypeBase(ContactTypeInput):
    pass
    
    class Config:
        orm_mode = True

class CreateContactType(ContactTypeBase):
    pass

class ContactTypeSchema(ContactTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]