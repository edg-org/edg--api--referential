from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

class HousingTypeInput(BaseModel):
    code: int
    name: str
    shortname: str

class HousingTypeUpdate(HousingTypeInput, metaclass=HideFields):
    class Config:
        fields_hided = {'code'}

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