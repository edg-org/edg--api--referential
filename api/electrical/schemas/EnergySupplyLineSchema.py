from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from api.configs.BaseModel import SchemaModel

class SupplyCoordinates(SchemaModel):
    altitude: float
    latitude: float
    longitude: float

class AgenciesServed(SchemaModel):
    code: int

class AreasServed(SchemaModel):
    code: int

class SupplyInfos(SchemaModel):
    name: str
    electrical_code: int
    line_type : str
    voltage_type: str
    real_voltage: float
    voltage_measurement_unit : str
    maximum_power: float
    power_measurement_unit: str
    departure_area_code: int
    departure_address: str
    is_owner : bool = True
    areas_served: Optional[List[AreasServed]] = None
    agencies_served: Optional[List[AgenciesServed]] = None
    coordinates: Optional[SupplyCoordinates] = None

class EnergySupplyLineSchema(SchemaModel):
    id: int
    code: int
    line_type_id: int
    voltage_type_id: int
    departure_area_id: int
    infos: SupplyInfos
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class CreateEnergySupplyLine(EnergySupplyLineSchema):
    class Config:
        fields_to_hide = {
            "id",
            "is_activated",
            "created_at",
            "updated_at"
        }

class EnergySupplyLineInput(CreateEnergySupplyLine):
    class Config:
        fields_to_hide = {
            "code",
            "line_type_id",
            "voltage_type_id",
            "departure_area_id"
        }
    
class EnergySupplyLineUpdate(SchemaModel):
    pass