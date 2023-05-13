from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from api.electrical.schemas.ConnectionPointSchema import ConnectionPointSchema

class TransformerCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class TransformerInfos(BaseModel):
    name: str
    brand: Optional[str]
    city_code: int
    area_code: Optional[int] = None
    tranformer_serial_number: Optional[str]
    manufacturing_country: Optional[str] = None
    coordinates: Optional[TransformerCoordinates] = None

class EnergySupplyLinesInfos(BaseModel):
    code: int
    is_active: bool

class TransformerUpdate(BaseModel):
    infos: TransformerInfos
    energy_supply_lines: List[EnergySupplyLinesInfos]

class TransformerInput(TransformerUpdate):
    pass


class TransformerBase(TransformerInput):
    transformer_code: str
    city_id: int
    area_id: Optional[int] = None
    supply_line_id: int

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