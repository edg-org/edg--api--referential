from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

class CityTypeInput(BaseModel):
    code: int
    name: str

class CityTypeUpdate(CityTypeInput, metaclass=HideFields):
    class Config:
        fields_hided = {'code'}

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