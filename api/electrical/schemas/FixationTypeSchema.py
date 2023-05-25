from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import OmitFields

class FixationTypeInput(BaseModel):
    code: int
    name: str

class FixationTypeUpdate(FixationTypeInput, metaclass=OmitFields):
    class Config:
        omit_fields = {'code'}

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