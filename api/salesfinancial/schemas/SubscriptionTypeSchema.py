from typing import List, Optional
from datetime import datetime, date
from api.configs.BaseModel import BaseSchema
from api.salesfinancial.schemas.PricingHistorySchema import PricingHistorySchema

class Dunning(BaseSchema):
    code: str
    rank: int
    name: str
    payment_deadline: int
    deadline_unit_time: str
    delay_penality_rate: float

class PricingSlices(BaseSchema):
    name: str
    unit_price: float
    lower_index: float
    upper_index: Optional[float] | None

class Pricing(BaseSchema):
    code: str
    name: str
    start_date: str
    # start_date: date
    subscription_fee: float
    slices: List[PricingSlices]

class PowerToSubscribe(BaseSchema):
    housing_type: str
    lower_power: float
    upper_power: float
    deposit_to_pay: float
    estimated_consumption: float

class TypeInfosBase(BaseSchema):
    tracking_type: str
    supply_mode: str
    payment_deadline: int
    deadline_measurement_unit: str
    tva: float
    currency: str
    consumption_frequency: str
    power_measurement_unit: str
    consumption_measurement_unit: str
    power_to_subscribe: List[PowerToSubscribe]

class SubscriptionTypeSchema(BaseSchema):
    id: Optional[int]
    code: str
    name: str
    infos: TypeInfosBase
    supply_mode_id: int
    tracking_type_id: int
    pricing: Pricing
    dunning: List[Dunning]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

class CreateSubscriptionType(SubscriptionTypeSchema):
    class Config:
        fields_to_hide = {
            "id",  
            "created_at",
            "updated_at"
        }

class SubscriptionTypeInput(CreateSubscriptionType):
    class Config:
        fields_to_hide = {
            "supply_mode_id", 
            "tracking_type_id"
        }

class SubscriptionTypeUpdate(SubscriptionTypeInput):
    pass

class SubscriptionTypeItemSchema(SubscriptionTypeSchema):
    pricing_histories: list[PricingHistorySchema] = []