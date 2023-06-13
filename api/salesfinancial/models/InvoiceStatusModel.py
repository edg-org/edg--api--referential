from datetime import datetime
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import (Column, DateTime, String)

class InvoiceStatusModel(EntityMeta):
    __tablename__ = "invoice_status"

    id = Column(TINYINT(unsigned=True), primary_key=True, index=True)
    code = Column(TINYINT(unsigned=True), index=True, unique=True, nullable=False)
    name = Column(String(100), index=True, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)