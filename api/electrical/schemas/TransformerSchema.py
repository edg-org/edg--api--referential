from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from api.electrical.schemas.ConnectionPoleSchema import ConnectionPoleSchema

class TransformerCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class EnergySupplyLines(BaseModel):
    electrical_code: int
    activation_dated: date
    desactivation_date: Optional[date]=None
    is_actived: bool

class TransformerInfos(BaseModel):
    name: str
    brand: Optional[str]
    power: float
    power_mesurement_unit: str
    fixation_type: str
    area_code: int
    electrical_code: int
    tranformer_serial_number: Optional[str]
    manufacturing_country: Optional[str] = None
    energy_supply_lines: List[EnergySupplyLines]
    address: Optional[str]
    coordinates: Optional[TransformerCoordinates] = None

class TransformerUpdate(BaseModel):
    infos: TransformerInfos

class TransformerInput(TransformerUpdate):
    pass

class TransformerBase(TransformerInput):
    transformer_code: str
    area_id: int
    fixation_type_id: int

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
    tranformers: list[ConnectionPoleSchema] = []