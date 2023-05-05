from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CityTypeBase(BaseModel):
    code: int
    name: str

    class Config:
        orm_mode = True

class CreateCityType(CityTypeBase):
    pass

class CityTypeSchema(CityTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]