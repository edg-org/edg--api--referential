from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.BaseModel import SchemaModel

#
class InvoicingFrequencySchema(SchemaModel):
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
    class Config:
        fields_to_hide = {"code"}

#
class InvoicingFrequencyUpdate(InvoicingFrequencyInput):
    pass