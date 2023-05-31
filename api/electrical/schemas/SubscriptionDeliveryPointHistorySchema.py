from pydantic import BaseModel
from datetime import datetime, date
from api.configs.Environment import HideFields

class SubscriptionHistorySchema(BaseModel):
    id: int
    contract_number: str
    delivery_point_number: str
    opening_date: date
    closing_date: date
    created_at: datetime
    
    class Config:
        orm_mode = True
    
class SubscriptionHistoryCreate(SubscriptionHistorySchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id",
            "created_at"
        }

class SubscriptionHistoryInput(SubscriptionHistoryCreate):
    pass