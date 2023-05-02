from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class MeterTypeBase(BaseModel):
    code: int
    name: str

    class Config:
        orm_mode = True


class CreateMeterType(MeterTypeBase):
    pass


class MeterTypeSchema(MeterTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
