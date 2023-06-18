from typing import Optional
from datetime import datetime
from api.configs.BaseModel import BaseSchema

#
class InvoicingFrequencySchema(BaseSchema):
    id: int
    code: int
    name: str
    shortname: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateInvoicingFrequency(InvoicingFrequencySchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class InvoicingFrequencyInput(CreateInvoicingFrequency):
    pass

#
class InvoicingFrequencyUpdate(InvoicingFrequencyInput):
    class Config:
        fields_to_hide = {"code"}