from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class EnergyDepartureCoordinates(BaseModel):
    altitude: str
    latitude: str
    longitude: str

class EnergyDepartureInfos(BaseModel):
    name: str
    address: str
    coordinates: EnergyDepartureCoordinates

class EnergyDepartureBase(BaseModel):
    code: int
    name: str
    infos: EnergyDepartureInfos
    
    class Config:
        orm_mode = True

class CreateEnergyDeparture(EnergyDepartureBase):
    pass

class EnergyDepartureSchema(EnergyDepartureBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]