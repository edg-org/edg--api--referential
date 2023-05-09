from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CityTypeUpdate(BaseModel):
    name: str

class CityTypeInput(CityTypeUpdate):
    code: int

class CityTypeBase(CityTypeInput):
    pass

    class Config:
        orm_mode = True

class CreateCityType(CityTypeBase):
    pass

class CityTypeSchema(CityTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]