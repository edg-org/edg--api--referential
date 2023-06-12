from typing import List
from datetime import datetime, date
from api.configs.BaseModel import BaseSchema

#
class MeterHistorySchema(BaseSchema):
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

#
class MeterHistoryPagination(BaseSchema):
    count: int
    total: int
    page_size: int
    start_index: int
    results: List[MeterHistorySchema] = []