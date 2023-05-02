from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class AreaTypeBase(BaseModel):
    code: int
    name: str

    class Config:
        orm_mode = True

class CreateAreaType(AreaTypeBase):
    pass

class AreaTypeSchema(AreaTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]