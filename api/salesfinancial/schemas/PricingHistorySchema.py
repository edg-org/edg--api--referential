from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date

class PricingSlices(BaseModel):
    name: str
    unit_price: float
    lower_index: float
    upper_index: Optional[float] | None

class PricingInfos(BaseModel):
    subscription_fee: float
    slices: List[PricingSlices]

class PricingHistoryInput(BaseModel):
    code: int
    name: str
    subscription_type_code: int
    start_date: date
    end_date: date
    infos: PricingInfos

class PricingHistoryBase(PricingHistoryInput):
    pass

    class Config:
        orm_mode = True

class CreatePricingHistory(PricingHistoryBase):
    pass

class PricingHistorySchema(PricingHistoryBase):
    id: int
    created_at: datetime