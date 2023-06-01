from typing import List, Optional
from datetime import datetime, date
from api.configs.BaseModel import SchemaModel

class PricingSlices(SchemaModel):
    name: str
    unit_price: float
    lower_index: float
    upper_index: Optional[float] | None

class PricingInfos(SchemaModel):
    subscription_fee: float
    slices: List[PricingSlices]
    

class PricingHistorySchema(SchemaModel):
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

class CreatePricingHistory(PricingHistorySchema):
     class Config:
        fields_to_hide = {
            "id",  
            "created_at"
        }
        
class PricingHistoryInput(CreatePricingHistory):
     pass