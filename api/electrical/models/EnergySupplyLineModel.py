from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT, MEDIUMINT, SMALLINT, BIGINT
from sqlalchemy import (
    JSON,
    Column,
    String,
    DateTime,
    Boolean,
    ForeignKey
)

class EnergySupplyLineModel(EntityMeta):
    __tablename__ = "energy_supply_lines"

    id = Column(TINYINT(unsigned=True), primary_key=True, index=True)
    code = Column(BIGINT(unsigned=True), index=True, unique=True, nullable=False)
    infos = Column(JSON, nullable=False)
    is_activated = Column(Boolean, index=True, default=True)
    departure_area_id = Column(MEDIUMINT(unsigned=True), ForeignKey("areas.id"), nullable=False)
    voltage_type_id = Column(TINYINT(unsigned=True), ForeignKey("voltage_types.id"), nullable=False)
    line_type_id = Column(TINYINT(unsigned=True), ForeignKey("supply_line_types.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)

    departure_area = relationship("AreaModel", back_populates="energy_supply_lines")
    voltage_type = relationship("VoltageTypeModel", back_populates="energy_supply_lines")
    supply_line_type = relationship("SupplyLineTypeModel", back_populates="energy_supply_lines")