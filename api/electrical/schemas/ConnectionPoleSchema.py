from typing import Optional, List
from datetime import datetime, date
from api.configs.BaseModel import SchemaModel
from api.ageographical.schemas.DeliveryPointSchema import DeliveryPointSchema

class PoleCoordinates(SchemaModel):
    altitude: float
    latitude: float
    longitude: float

class Transformers(SchemaModel):
    electrical_code: int
    activation_dated: date
    desactivation_date: Optional[date]=None
    is_actived: bool
    
class PoleInfos(SchemaModel):
    number: int
    name: Optional[str]=None
    area_code: int
    electrical_code: int
    transformer_code: int
    address: str
    transformers: List[Transformers]
    coordinates: Optional[PoleCoordinates]=None
    

class ConnectionPoleSchema(SchemaModel):
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

class CreateConnectionPole(ConnectionPoleSchema):
    class Config:
        fields_to_hide = {
            "id",
            "is_activated",
            "created_at",
            "updated_at",
            "deleted_at"
        }

class ConnectionPoleInput(CreateConnectionPole):
    class Config:
        fields_to_hide = {
            "transformer_id",
            "pole_number",
            "area_id"
        }

class ConnectionPoleUpdate(ConnectionPoleInput):
    pass

class ConnectionPoleItemSchema(ConnectionPoleSchema):
    deliverypoints: list[DeliveryPointSchema] = []