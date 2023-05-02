from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ContactTypeBase(BaseModel):
    code: int
    name: str
    
    class Config:
        orm_mode = True

class CreateContactType(ContactTypeBase):
    pass

class ContactTypeSchema(ContactTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]