from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

class AreaTypeInput(BaseModel):
    code: int
    name: str

class AreaTypeUpdate(AreaTypeInput, metaclass=HideFields):
    class Config:
        fields_hided = {'code'}

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