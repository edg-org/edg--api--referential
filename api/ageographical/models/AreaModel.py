from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import (
    TINYINT,
    SMALLINT,
    MEDIUMINT,
    BIGINT
)
from sqlalchemy import (
    Column,
    JSON,
    Boolean,
    Integer,
    String,
    DateTime,
    ForeignKey
)

class AreaModel(EntityMeta):
    __tablename__ = "areas"

    id = Column(MEDIUMINT(unsigned=True), primary_key=True, index=True,)
    code = Column(BIGINT(unsigned=True), index=True, unique=True, nullable=False)
    city_id = Column(SMALLINT(unsigned=True), ForeignKey("cities.id"), nullable=False)
    agency_id = Column(SMALLINT(unsigned=True), ForeignKey("agencies.id"), nullable=True)
    hierarchical_area_id = Column(MEDIUMINT(unsigned=True), ForeignKey("areas.id"), nullable=True)
    area_type_id = Column(TINYINT(unsigned=True), ForeignKey("area_types.id"), nullable=False)
    zipcode = Column(String(5), index=True, unique=False, nullable=False)
    infos = Column(JSON, nullable=False)
    is_activated = Column(Boolean, index=True, default=True)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    city = relationship("CityModel", back_populates="areas")
    agency = relationship("AgencyModel", back_populates="areas")
    area_type = relationship("AreaTypeModel", back_populates="areas")

    transformers = relationship("TransformerModel", back_populates="area")
    delivery_points = relationship("DeliveryPointModel", back_populates="area")
    connection_points = relationship("ConnectionPointModel", back_populates="area")