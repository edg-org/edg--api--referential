from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class SupplyCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class AgenciesServed(BaseModel):
    code: int


class SupplyInfos(BaseModel):
    name: str
    line_type : str
    is_owner : bool = True,
    real_power: float
    power_measurement_unit : str
    departure_city_code: int
    agencies_served: Optional[List[AgenciesServed]] = None
    address: Optional[str] = None
    coordinates: Optional[SupplyCoordinates] = None

class EnergySupplyLineUpdate(BaseModel):
    infos: SupplyInfos

class EnergySupplyLineInput(EnergySupplyLineUpdate):
    pass

class EnergySupplyLineBase(EnergySupplyLineInput):
    code: int
    departure_city_id: int
    line_type_id: int

    class Config:
        orm_mode = True

class CreateEnergySupplyLine(EnergySupplyLineBase):
    pass

class EnergySupplyLineSchema(EnergySupplyLineBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]