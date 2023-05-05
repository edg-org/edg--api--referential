from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.electrical.schemas.ConnectionPointSchema import ConnectionPointSchema

class TransformerCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class TransformerInfos(BaseModel):
    name: Optional[str]
    area_code: Optional[int]
    city_code: Optional[int]
    factory_name: str
    index_reading: float
    manufacturing_country: str
    coordinates: TransformerCoordinates

class TransformerBase(BaseModel):
    tranformer_number: str
    departure_id: int
    area_id: Optional[int]
    city_id: Optional[int]
    infos: TransformerInfos

    class Config:
        orm_mode = True

class CreateTransformer(TransformerBase):
    pass

class TransformerSchema(TransformerBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

class TransformerItemSchema(TransformerSchema):
    tranformers: list[ConnectionPointSchema] = []