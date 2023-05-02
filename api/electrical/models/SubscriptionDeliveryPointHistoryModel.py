from datetime import datetime
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import (Column, DateTime, Date, String, UniqueConstraint)

class SubscriptionDeliveryPointHistoryModel(EntityMeta):
    __tablename__ = "subscription_delivery_point_histories"

    id = Column(TINYINT(unsigned=True), primary_key=True, index=True)
    contract_number = Column(TINYINT(unsigned=True), index=True, unique=True, nullable=False)
    delivery_point_number = Column(String(20), index=True, unique=True, nullable=False)
    opening_date = Column(Date, nullable=False)
    closing_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    UniqueConstraint("contract_number", "delivery_point_number", "opening_date", name="uix1_sdph")