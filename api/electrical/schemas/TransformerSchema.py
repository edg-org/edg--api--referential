from typing import Optional, List
from datetime import date, datetime
from api.configs.BaseModel import BaseSchema
from api.electrical.schemas.ConnectionPoleSchema import ConnectionPoleSchema
from sqlalchemy.sql import func

#
class TransformerCoordinates(BaseSchema):
    altitude: float
    latitude: float
    longitude: float

#
class EnergySupplyLines(BaseSchema):
    electrical_code: int = 0
    is_activated: bool = False
    activation_date: Optional[str]
    desactivation_date: Optional[str]
    # activation_date: Optional[date]
    # activation_date: date = func.now()
    # desactivation_date: Optional[date]

#
class TransformerInfos(BaseSchema):
    name: Optional[str]
    brand: Optional[str]
    power: Optional[float]
    power_mesurement_unit: Optional[str]
    fixation_type: Optional[str]
    area_code: Optional[int]
    electrical_code: Optional[int]
    tranformer_serial_number: Optional[str]
    manufacturing_country: Optional[str] = None
    address: Optional[str]
    coordinates: Optional[TransformerCoordinates] = None

class TransformerSchema(BaseSchema):
    id: Optional[int]
    transformer_code: Optional[str]
    area_id: Optional[int]
    fixation_type_id: Optional[int]
    infos: TransformerInfos
    energy_supply_lines: Optional[List[EnergySupplyLines]]
    is_activated: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True

class CreateTransformer(TransformerSchema):
    class Config:
        fields_to_hide = {
            "id",
            "is_activated",
            "created_at",
            "updated_at",
            "deleted_at"
        }
        
#
class TransformerInput(CreateTransformer):
    class Config:
        fields_to_hide = {
            "area_id",
            "transformer_code",
            "fixation_type_id"
        }



class TransformerUpdate(TransformerInput):
    pass

#
class TransformerItemSchema(TransformerSchema):
    tranformers: list[ConnectionPoleSchema] = []