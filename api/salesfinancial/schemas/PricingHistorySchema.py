from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date
from api.configs.Environment import HideFields

class PricingSlices(BaseModel):
    name: str
    unit_price: float
    lower_index: float
    upper_index: Optional[float] | None

class PricingInfos(BaseModel):
    subscription_fee: float
    slices: List[PricingSlices]
    

class PricingHistorySchema(BaseModel):
    id: int
    code: int
    name: str
    subscription_type_code: int
    start_date: date
    end_date: date
    infos: PricingInfos
    created_at: datetime
    
    class Config:
        orm_mode = True

class CreatePricingHistory(PricingHistorySchema, metaclass=HideFields):
     class Config:
        fields_hided = {
            "id",  
            "created_at"
        }
        
class PricingHistoryInput(CreatePricingHistory):
     pass