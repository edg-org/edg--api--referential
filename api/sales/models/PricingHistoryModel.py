from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import (Column, DateTime, Date, JSON, String)

class PricingHistoryModel(EntityMeta):
    __tablename__ = "pricing_histories"

    id = Column(TINYINT(unsigned=True), primary_key=True, index=True)
    code = Column(TINYINT(unsigned=True), index=True, unique=True, nullable=False)
    name = Column(String(20), index=True, unique=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    infos = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)

    subscription_type = relationship("SubscriptionTypeModel", back_populates="pricing_histories")