from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

class MeterTypeInput(BaseModel):
    code: int
    name: str

class MeterTypeUpdate(MeterTypeInput, metaclass=HideFields):
    class Config:
        fields_hided = {'code'}

class MeterTypeBase(MeterTypeInput):
    pass

    class Config:
        orm_mode = True

class CreateMeterType(MeterTypeBase):
    pass

class MeterTypeSchema(MeterTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]