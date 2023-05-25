from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from api.ageographical.schemas.CitySchema import CitySchema

class PrefectureSearchParams(BaseModel):
    code: int = Field(description="Field of the prefecture code")
    name: str | None = Field(description="Field of the prefecture name")

class PrefectureCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class PrefectureInfos(BaseModel):
    region: str
    coordinates: Optional[PrefectureCoordinates]

class PrefectureInput(BaseModel):
    name: str
    is_capital: bool
    infos: PrefectureInfos

class PrefectureUpdate(PrefectureInput):
    pass

class PrefectureBase(PrefectureInput):
    code: int
    region_id: int
    prefecture_number: str

    class Config:
        orm_mode = True

class CreatePrefecture(PrefectureBase):
    pass

class PrefectureSchema(PrefectureBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

class PrefectureItemSchema(PrefectureSchema):
    cities: list[CitySchema] = []