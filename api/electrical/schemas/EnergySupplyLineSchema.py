from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class SupplyCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class SupplyInfos(BaseModel):
    name: str
    line_type : str
    real_supply_power: float
    measurement_unit : str
    departure_city_code: int
    arrival_city_code: Optional[int] = None
    address: str
    coordinates: Optional[SupplyCoordinates] = None

class EnergySupplyLineUpdate(BaseModel):
    infos: SupplyInfos

class EnergySupplyLineInput(EnergySupplyLineUpdate):
    pass

class EnergySupplyLineBase(EnergySupplyLineInput):
    code: int
    departure_city_id: int
    arrival_city_id: int
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