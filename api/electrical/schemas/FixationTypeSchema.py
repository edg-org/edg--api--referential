from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

class FixationTypeInput(BaseModel):
    code: int
    name: str

class FixationTypeUpdate(FixationTypeInput, metaclass=HideFields):
    class Config:
        fields_hided = {'code'}

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