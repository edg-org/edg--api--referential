from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CityLevelBase(BaseModel):
    code: int
    name: str

    class Config:
        orm_mode = True

class CreateCityLevel(CityLevelBase):
    pass

class CityLevelSchema(CityLevelBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]