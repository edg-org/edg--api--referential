from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import (Column, DateTime, JSON, String, ForeignKey)

class SubscriptionTypeModel(EntityMeta):
    __tablename__ = "subscription_types"

    id = Column(TINYINT(unsigned=True), primary_key=True, index=True)
    code = Column(TINYINT(unsigned=True), index=True, unique=True, nullable=False)
    name = Column(String(20), index=True, unique=True, nullable=False)
    infos = Column(JSON, nullable=False)
    pricing = Column(JSON, nullable=False)
    dunning = Column(JSON, nullable=False)
    tracking_id = Column(TINYINT(unsigned=True), ForeignKey("tracking_types.id"), nullable=False)
    power_mode_id = Column(TINYINT(unsigned=True), ForeignKey("power_modes.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    tracking_type = relationship("TrackingTypeModel", back_populates="subscription_types")
    power_mode = relationship("MeterPowerModeModel", back_populates="subscription_types")

    pricing_histories = relationship("PricingHistoryModel", back_populates="subscription_type")