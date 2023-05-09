from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class InvoicingFrequencyUpdate(BaseModel):
    name: str
    shortname: str

class InvoicingFrequencyInput(InvoicingFrequencyUpdate):
    code: int

class InvoicingFrequencyBase(InvoicingFrequencyInput):
    pass
    
    class Config:
        orm_mode = True

class CreateInvoicingFrequency(InvoicingFrequencyBase):
    pass

class InvoicingFrequencySchema(InvoicingFrequencyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]