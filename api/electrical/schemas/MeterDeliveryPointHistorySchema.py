from pydantic import BaseModel
from datetime import datetime, date
from api.configs.BaseModel import SchemaModel

#
class MeterHistorySchema(SchemaModel):
    id: int
    meter_number: str
    delivery_point_number: str
    installation_date: date
    uninstallation_date: date
    created_at: datetime
    
    class Config:
        orm_mode = True
 
 #   
class MeterHistoryCreate(MeterHistorySchema):
    class Config:
        fields_to_hide = {
            "id",
            "created_at"
        }

#
class MeterHistoryInput(MeterHistoryCreate):
    pass