from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.BaseModel import SchemaModel

#
class ElectricMeterInfos(SchemaModel):
    brand: str
    meter_type: str
    supply_mode: str
    index_reading: float
    manufacturing_country: str

#
class ElectricMeterSchema(SchemaModel):
    id: int
    meter_number: str
    infos: ElectricMeterInfos
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        orm_mode = True
    
#
class CreateElectricMeter(ElectricMeterSchema):
    class Config:
        fields_to_hide = {
            "id",
            "is_activated",
            "created_at",
            "updated_at",
            "deleted_at"
        }

#
class ElectricMeterInput(ElectricMeterSchema):
    class Config:
        fields_to_hide = {"meter_number"}

#
class ElectricMeterUpdate(ElectricMeterInput):
    pass