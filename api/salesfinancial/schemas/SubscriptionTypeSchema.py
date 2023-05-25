from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date
from pydantic.dataclasses import dataclass
from api.configs.Environment import OmitFields
from api.salesfinancial.schemas.PricingHistorySchema import PricingHistorySchema

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
    start_date: date
    subscription_fee: float
    slices: List[PricingSlices]


class PowerToSubscribe(BaseModel):
    housing_type: str
    lower_power: float
    upper_power: float
    deposit_to_pay: float
    estimated_consumption: float

class TypeInfosBase(BaseModel):
    payment_deadline: int
    deadline_measurement_unit: str
    tva: float
    currency: str
    consumption_frequency: str
    power_measurement_unit: str
    consumption_measurement_unit: str
    power_to_subscribe: List[PowerToSubscribe]

class TypeInfosInput(TypeInfosBase):
    tracking_type: str
    supply_mode: str

class SubscriptionTypeInput(BaseModel):
    code: str
    name: str
    infos: TypeInfosBase
    pricing: Pricing
    dunning: List[Dunning]

class SubscriptionTypeUpdate(SubscriptionTypeInput, metaclass=OmitFields):
    class Config:
        omit_fields = {'code'}
        arbitrary_types_allowed = True

class SubscriptionTypeBase(SubscriptionTypeInput):
    supply_mode_id: int
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
