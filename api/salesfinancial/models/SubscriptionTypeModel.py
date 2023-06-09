from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import (Column, DateTime, JSON, String, ForeignKey)

class SubscriptionTypeModel(EntityMeta):
    __tablename__ = "subscription_types"

    id = Column(TINYINT(unsigned=True), primary_key=True, index=True)
    code = Column(String(10), index=True, unique=True, nullable=False)
    name = Column(String(100), index=True, unique=True, nullable=False)
    infos = Column(JSON, nullable=False)
    pricing = Column(JSON, nullable=False)
    dunning = Column(JSON, nullable=False)
    tracking_type_id = Column(TINYINT(unsigned=True), ForeignKey("tracking_types.id"), nullable=False)
    supply_mode_id = Column(TINYINT(unsigned=True), ForeignKey("supply_modes.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    supply_mode = relationship("SupplyModeModel", back_populates="subscription_types")
    tracking_type = relationship("TrackingTypeModel", back_populates="subscription_types")