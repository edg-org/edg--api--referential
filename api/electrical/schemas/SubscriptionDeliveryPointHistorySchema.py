from datetime import datetime, date
from api.configs.BaseModel import SchemaModel

class SubscriptionHistorySchema(SchemaModel):
    id: int
    contract_number: str
    delivery_point_number: str
    opening_date: date
    closing_date: date
    created_at: datetime
    
    class Config:
        orm_mode = True
    
class SubscriptionHistoryCreate(SubscriptionHistorySchema):
    class Config:
        fields_to_hide = {
            "id",
            "created_at"
        }

class SubscriptionHistoryInput(SubscriptionHistoryCreate):
    pass