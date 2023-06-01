from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from api.configs.BaseModel import SchemaModel
from api.electrical.schemas.ConnectionPoleSchema import ConnectionPoleSchema

#
class TransformerCoordinates(SchemaModel):
    altitude: float
    latitude: float
    longitude: float

#
class EnergySupplyLines(SchemaModel):
    electrical_code: int
    is_actived: bool
    activation_dated: date
    desactivation_date: Optional[date]=None

#
class TransformerInfos(SchemaModel):
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

#
class TransformerSchema(SchemaModel):
    id: int
    transformer_code: str
    area_id: int
    fixation_type_id: int
    infos: TransformerInfos
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True

#
class CreateTransformer(TransformerSchema):
    class Config:
        fields_to_hide = {
            "id",
            "created_at",
            "updated_at",
            "deleted_at"
        }
        
#
class TransformerInput(CreateTransformer):
    class Config:
        fields_to_hide = {
            "transformer_code",
            "area_id",
            "fixation_type_id"
        }

#
class TransformerUpdate(TransformerInput):
    pass

#
class TransformerItemSchema(TransformerSchema):
    tranformers: list[ConnectionPoleSchema] = []