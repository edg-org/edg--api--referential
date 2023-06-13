from typing import Optional
from datetime import datetime
from api.configs.BaseModel import BaseSchema

#
class ElectricMeterInfos(BaseSchema):
    brand: Optional[str]
    meter_type: Optional[str]
    supply_mode: Optional[str]
    index_reading: Optional[float]
    manufacturing_country: Optional[str]

#
class ElectricMeterSchema(BaseSchema):
    id: Optional[int]
    meter_number: Optional[str]
    supply_mode_id: Optional[int]
    meter_type_id: Optional[int]
    infos: Optional[ElectricMeterInfos]
    is_activated: bool = True
    created_at: Optional[datetime]
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
class ElectricMeterInput(CreateElectricMeter):
    class Config:
        fields_to_hide = {"supply_mode_id","meter_type_id"}

#
class ElectricMeterUpdate(ElectricMeterInput):
    pass