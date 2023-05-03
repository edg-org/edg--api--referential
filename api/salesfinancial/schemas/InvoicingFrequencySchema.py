from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class InvoicingFrequencyBase(BaseModel):
    code: int
    name: str
    shortname: str
    
    class Config:
        orm_mode = True

class CreateInvoicingFrequency(InvoicingFrequencyBase):
    pass

class InvoicingFrequencySchema(InvoicingFrequencyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]