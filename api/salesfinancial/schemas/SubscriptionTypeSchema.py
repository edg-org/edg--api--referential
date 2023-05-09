from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date
from api.salesfinancial.schemas.PricingHistorySchema import (
    PricingHistorySchema,
)


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
    name: str
    subscription_fee: float
    start_date: date
    slices: List[PricingSlices]


class PowerToSubscribe(BaseModel):
    lower_power: float
    upper_power: float
    estimated_consumption: float
    deposit_to_pay: float

class TypeInfosBase(BaseModel):
    payment_deadline: int
    deadline_measurement_unit: str
    tva: float
    currency: str
    power_measurement_unit: str
    power_to_subscribe: List[PowerToSubscribe]

class TypeInfosInput(TypeInfosBase):
    tracking_type: str
    power_mode: str

class SubscriptionTypeUpdate(BaseModel):
    name: str
    infos: TypeInfosBase
    pricing: Pricing
    dunning: List[Dunning]

class SubscriptionTypeInput(SubscriptionTypeUpdate):
    code: int
    name: str
    infos: TypeInfosInput
    pricing: Pricing
    dunning: List[Dunning]

class SubscriptionTypeBase(SubscriptionTypeInput):
    power_mode_id: int
    tracking_type_id: int

    class Config:
        orm_mode = True


class CreateSubscriptionType(SubscriptionTypeBase):
    pass


class SubscriptionTypeSchema(SubscriptionTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]


class SubscriptionTypeItemSchema(SubscriptionTypeSchema):
    pricing_histories: list[PricingHistorySchema] = []
