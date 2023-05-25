from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import OmitFields

class InvoicingFrequencyInput(BaseModel):
    code: int
    name: str
    shortname: str

class InvoicingFrequencyUpdate(InvoicingFrequencyInput, metaclass=OmitFields):
    class Config:
        omit_fields = {'code'}

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