from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class MeterTypeUpdate(BaseModel):
    name: str

class MeterTypeInput(MeterTypeUpdate):
    code: int

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