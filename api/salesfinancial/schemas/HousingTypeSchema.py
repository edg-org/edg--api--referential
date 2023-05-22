from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class HousingTypeUpdate(BaseModel):
    name: str
    shortname: str

class HousingTypeInput(HousingTypeUpdate):
    code: int

class HousingTypeBase(HousingTypeInput):
    pass

    class Config:
        orm_mode = True

class CreateHousingType(HousingTypeBase):
    pass

class HousingTypeSchema(HousingTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]