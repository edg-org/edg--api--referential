from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ContactTypeUpdate(BaseModel):
    name: str

class ContactTypeInput(ContactTypeUpdate):
    code: int

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