from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, BIGINT
from sqlalchemy import (
    JSON,
    Column,
    String,
    DateTime,
    ForeignKey,
)


class EnergySupplyLineModel(EntityMeta):
    __tablename__ = "energy_supply_lines"

    id = Column(TINYINT(unsigned=True), primary_key=True, index=True)
    code = Column(BIGINT(unsigned=True), index=True, unique=True, nullable=False)
    infos = Column(JSON, nullable=False)
    departure_city_id = Column(SMALLINT(unsigned=True), ForeignKey("cities.id"), nullable=True)
    arrival_city_id = Column(SMALLINT(unsigned=True), nullable=True)
    line_type_id = Column(TINYINT(unsigned=True), ForeignKey("supply_line_types.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)

    departure_city = relationship("CityModel", back_populates="departure_supply_lines")
    supply_line_type = relationship("SupplyLineTypeModel", back_populates="energy_supply_lines")