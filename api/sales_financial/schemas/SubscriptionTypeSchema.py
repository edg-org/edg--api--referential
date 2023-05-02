from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date
from api.sales_financial.schemas.PricingHistorySchema import PricingHistorySchema

class Dunning(BaseModel):
    code: str
    rank: int
    name: str
    payment_deadline: int
    deadline_unit_time: str
    delay_penality_rate: float

class PricingSlices(BaseModel):
    name: str
    unit_price: float
    lower_index: float
    upper_index: Optional[float] | None

class Pricing(BaseModel):
    code: str
    name : str
    subscription_fee: float
    start_date: date
    slices: List[PricingSlices]

class PowerToSubscribe(BaseModel):
    power: float
    deposit_to_pay: float

class TypeInfos(BaseModel):
    payment_deadline: int
    deadline_measurement_unit: str
    tva: float
    currency: str
    power_to_subscribe: List[PowerToSubscribe]

class SubscriptionTypeBase(BaseModel):
    code: int
    name: str
    tracking_type_id: int
    power_mode_id: int
    infos: TypeInfos
    pricing: Pricing
    dunning: List[Dunning]

    class Config:
        orm_mode = True

class CreateSubscriptionType(SubscriptionTypeBase):
    pass

class SubscriptionTypeSchema(SubscriptionTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

class SubscriptionTypeItemSchema(SubscriptionTypeSchema):
    pricing_histories : list[PricingHistorySchema] = []