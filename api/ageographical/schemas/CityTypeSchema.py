from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import OmitFields

class CityTypeInput(BaseModel):
    code: int
    name: str

class CityTypeUpdate(CityTypeInput, metaclass=OmitFields):
    class Config:
        omit_fields = {'code'}

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