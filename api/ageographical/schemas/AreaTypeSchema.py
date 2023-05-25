from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import OmitFields

class AreaTypeInput(BaseModel):
    code: int
    name: str

class AreaTypeUpdate(AreaTypeInput, metaclass=OmitFields):
    class Config:
        omit_fields = {'code'}

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