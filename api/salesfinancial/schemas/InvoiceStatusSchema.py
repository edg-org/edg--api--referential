from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class InvoiceStatusUpdate(BaseModel):
    name: str

class InvoiceStatusInput(InvoiceStatusUpdate):
    code: int

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