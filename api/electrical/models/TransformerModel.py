from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, MEDIUMINT
from sqlalchemy import (
    Column,
    DateTime,
    JSON,
    String,
    ForeignKey,
)

#
class TransformerModel(EntityMeta):
    __tablename__ = "transformers"

    id = Column(MEDIUMINT(unsigned=True), primary_key=True, index=True)
    transformer_code = Column(String(15), index=True, unique=True, nullable=False)
    energy_supply_lines = Column(JSON, nullable=False)
    infos = Column(JSON, nullable=False)
    city_id = Column(SMALLINT(unsigned=True), ForeignKey("cities.id"), nullable=False)
    area_id = Column(MEDIUMINT(unsigned=True), ForeignKey("areas.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)

    city = relationship("CityModel", back_populates="transformers")
    area = relationship("AreaModel", back_populates="transformers")
    
    connection_points = relationship("ConnectionPointModel", back_populates="transformer")