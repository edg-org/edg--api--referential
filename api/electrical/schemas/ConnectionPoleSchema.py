from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional, List
from api.configs.Environment import HideFields
from api.ageographical.schemas.DeliveryPointSchema import DeliveryPointSchema

class PoleCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class Transformers(BaseModel):
    electrical_code: int
    activation_dated: date
    desactivation_date: Optional[date]=None
    is_actived: bool
    
class PoleInfos(BaseModel):
    number: int
    name: Optional[str]=None
    area_code: int
    electrical_code: int
    transformer_code: int
    address: str
    transformers: List[Transformers]
    coordinates: Optional[PoleCoordinates]=None
    

class ConnectionPoleSchema(BaseModel):
    id: int
    pole_number: str
    transformer_id: int
    area_id: int
    infos: PoleInfos
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True

class CreateConnectionPole(ConnectionPoleSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id",
            "is_activated",
            "created_at",
            "updated_at",
            "deleted_at"
        }

class ConnectionPoleInput(CreateConnectionPole, metaclass=HideFields):
    class Config:
        fields_hided = {
            "transformer_id",
            "pole_number",
            "area_id"
        }

class ConnectionPoleUpdate(ConnectionPoleInput):
    pass

class ConnectionPoleItemSchema(ConnectionPoleSchema):
    deliverypoints: list[DeliveryPointSchema] = []