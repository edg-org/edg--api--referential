from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import OmitFields

class CityLevelInput(BaseModel):
    name: str
    code: int

class CityLevelUpdate(CityLevelInput):
    class Config:
        omit_fields = {'code'}

class CityLevelBase(CityLevelInput, metaclass=OmitFields):
    pass

    class Config:
        orm_mode = True

class CreateCityLevel(CityLevelBase):
    pass

class CityLevelSchema(CityLevelBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]