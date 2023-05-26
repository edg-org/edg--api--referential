from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

class InvoiceStatusInput(BaseModel):
    code: int
    name: str

class InvoiceStatusUpdate(InvoiceStatusInput, metaclass=HideFields):
    class Config:
        fields_hided = {'code'}

class InvoiceStatusBase(InvoiceStatusInput):
    pass
    
    class Config:
        orm_mode = True

class CreateInvoiceStatus(InvoiceStatusBase):
    pass

class InvoiceStatusSchema(InvoiceStatusBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]