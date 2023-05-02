from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import (Column, DateTime, JSON, String, ForeignKey)

class MeterTypeModel(EntityMeta):
    __tablename__ = "electric_meters"

    id = Column(TINYINT(unsigned=True), primary_key=True, index=True)
    metric_number = Column(String(15), index=True, unique=True, nullable=False)
    power_mode_id = Column(TINYINT(unsigned=True), ForeignKey("power_modes.id"), nullable=False)
    type_id = Column(TINYINT(unsigned=True), ForeignKey("meter_types.id"), nullable=False)
    metric_number = Column(String(15), index=True, unique=True, nullable=False)
    infos = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)
    
    meter_type = relationship("MeterTypeModel", back_populates="electric_meters")
    power_mode = relationship("PowerModeModel", back_populates="electric_meters")

    meters = relationship("ElectricMeterModel", back_populates="meter_type")

    meter_delivery_points = relationship("MeterDeliveryPointModel", back_populates="electric_meter")