from datetime import date, datetime
from typing import Optional, List, Dict
from api.configs.BaseModel import BaseSchema

class DeliveryCoordinates(BaseSchema):
    altitude: float
    latitude: float
    longitude: float

class DeliveryInfos(BaseSchema):
    number: int
    area_code: int
    electrical_code: int
    pole_number: int
    address: str
    coordinates: Optional[DeliveryCoordinates]

class ConnectionPole(BaseSchema):
    electrical_code: int
    activation_date: date
    desactivation_date: Optional[date]=None
    is_actived: bool
    
class DeliveryPointSchema(BaseSchema):
    id: int
    delivery_point_number: int
    infos: DeliveryInfos
    connection_poles: List[ConnectionPole]
    area_id: int
    pole_id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        orm_mode = True
    
class CreateDeliveryPoint(DeliveryPointSchema):
    class Config:
        fields_to_hide = {
            "id",
            "is_activated",
            "created_at",
            "updated_at",
            "deleted_at",
        }

#
class DeliveryPointInput(CreateDeliveryPoint):
    class Config:
        fields_to_hide = {
            "id",
            "area_id",
            "pole_id",
            "delivery_point_number"
        }
 
 #   
class DeliveryPointUpdate(DeliveryPointInput):
 pass


class DeliveryPointDetails(CreateDeliveryPoint):
    details: Dict
    class Config:
        fields_to_hide = {
            "id",
            "area_id",
            "pole_id",
            "infos"
        }

#
class DeliveryPointPagination(BaseSchema):
    count: int
    total: int
    page_size: int
    start_index: int
    results: List[DeliveryPointSchema] = []