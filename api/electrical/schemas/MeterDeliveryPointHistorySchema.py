from pydantic import BaseModel
from datetime import datetime, date
from api.configs.Environment import HideFields

#
class MeterHistorySchema(BaseModel):
    id: int
    meter_number: str
    delivery_point_number: str
    installation_date: date
    uninstallation_date: date
    created_at: datetime
    
    class Config:
        orm_mode = True
 
 #   
class MeterHistoryCreate(MeterHistorySchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id",
            "created_at"
        }

#
class MeterHistoryInput(MeterHistoryCreate):
    pass