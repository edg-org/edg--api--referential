from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.electrical.schemas.TransformerSchema import (
    TransformerSchema,
)


class DepartureCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float


class DepartureInfos(BaseModel):
    name: str
    address: str
    coordinates: DepartureCoordinates


class EnergyDepartureBase(BaseModel):
    code: str
    area_id: int
    infos: DepartureInfos

    class Config:
        orm_mode = True


class CreateEnergyDeparture(EnergyDepartureBase):
    pass


class EnergyDepartureSchema(EnergyDepartureBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]


class EnergyDepartureItemSchema(EnergyDepartureSchema):
    tranformers: list[TransformerSchema] = []
