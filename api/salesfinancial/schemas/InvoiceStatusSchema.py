from typing import Optional
from datetime import datetime
from api.configs.BaseModel import SchemaModel

class InvoiceStatusSchema(SchemaModel):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateInvoiceStatus(InvoiceStatusSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class InvoiceStatusInput(CreateInvoiceStatus):
    class Config:
        fields_to_hide = {"code"}

#
class InvoiceStatusUpdate(InvoiceStatusInput):
    pass