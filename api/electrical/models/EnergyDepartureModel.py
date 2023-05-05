from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, MEDIUMINT
from sqlalchemy import (
    JSON,
    Column,
    String,
    DateTime,
    ForeignKey,
)


class EnergyDepartureModel(EntityMeta):
    __tablename__ = "energy_departures"

    id = Column(TINYINT(unsigned=True), primary_key=True, index=True)
    code = Column(String(15), index=True, unique=True, nullable=False)
    city_id = Column(SMALLINT(unsigned=True), ForeignKey("areas.id"), nullable=True)
    area_id = Column(MEDIUMINT(unsigned=True), ForeignKey("areas.id"), nullable=True)
    infos = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)

    city = relationship("CityModel", back_populates="transformers")
    area = relationship("AreaModel", back_populates="energy_departures")

    transformers = relationship("TransformerModel", back_populates="energy_departure")
