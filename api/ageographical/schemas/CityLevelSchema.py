from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

class CityLevelInput(BaseModel):
    name: str
    code: int

class CityLevelUpdate(CityLevelInput):
    class Config:
        fields_hided = {'code'}

class CityLevelBase(CityLevelInput, metaclass=HideFields):
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