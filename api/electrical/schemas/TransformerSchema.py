from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from api.configs.Environment import HideFields
from api.electrical.schemas.ConnectionPoleSchema import ConnectionPoleSchema

#
class TransformerCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

#
class EnergySupplyLines(BaseModel):
    electrical_code: int
    activation_dated: date
    desactivation_date: Optional[date]=None
    is_actived: bool

#
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

#
class TransformerSchema(BaseModel):
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
class CreateTransformer(TransformerSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id",
            "created_at",
            "updated_at",
            "deleted_at"
        }
        
#
class TransformerInput(CreateTransformer, metaclass=HideFields):
    class Config:
        fields_hided = {
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