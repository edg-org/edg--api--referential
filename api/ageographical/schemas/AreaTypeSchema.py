from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class AreaTypeUpdate(BaseModel):
    name: str

class AreaTypeInput(AreaTypeUpdate):
    code: int

class AreaTypeBase(AreaTypeInput):
    pass

    class Config:
        orm_mode = True

class CreateAreaType(AreaTypeBase):
    pass

class AreaTypeSchema(AreaTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]