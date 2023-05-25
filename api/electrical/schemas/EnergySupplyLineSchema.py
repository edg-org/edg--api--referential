from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class SupplyCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class AgenciesServed(BaseModel):
    code: int

class AreasServed(BaseModel):
    code: int

class SupplyInfos(BaseModel):
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

class EnergySupplyLineUpdate(BaseModel):
    infos: SupplyInfos

class EnergySupplyLineInput(EnergySupplyLineUpdate):
    pass

class EnergySupplyLineBase(EnergySupplyLineInput):
    code: int
    line_type_id: int
    voltage_type_id: int
    departure_area_id: int

    class Config:
        orm_mode = True

class CreateEnergySupplyLine(EnergySupplyLineBase):
    pass

class EnergySupplyLineSchema(EnergySupplyLineBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]