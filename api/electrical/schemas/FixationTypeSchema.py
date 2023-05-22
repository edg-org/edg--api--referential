from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class FixationTypeUpdate(BaseModel):
    name: str

class FixationTypeInput(FixationTypeUpdate):
    code: int

class FixationTypeBase(FixationTypeInput):
    pass

    class Config:
        orm_mode = True

class CreateFixationType(FixationTypeBase):
    pass

class FixationTypeSchema(FixationTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]