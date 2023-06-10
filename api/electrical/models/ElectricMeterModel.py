from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT, MEDIUMINT
from sqlalchemy import (
    Column,
    DateTime,
    JSON,
    String,
    Boolean,
    ForeignKey
)

class ElectricMeterModel(EntityMeta):
    __tablename__ = "electric_meters"

    id = Column(MEDIUMINT(unsigned=True), primary_key=True, index=True)
    meter_number = Column(String(15), index=True, unique=True, nullable=False)
    infos = Column(JSON, nullable=False)
    supply_mode_id = Column(TINYINT(unsigned=True), ForeignKey("supply_modes.id"), nullable=False)
    meter_type_id = Column(TINYINT(unsigned=True), ForeignKey("meter_types.id"), nullable=False)
    is_activated = Column(Boolean, index=True, default=True)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)

    meter_type = relationship("MeterTypeModel", back_populates="electric_meters")
    supply_mode = relationship("SupplyModeModel", back_populates="electric_meters")