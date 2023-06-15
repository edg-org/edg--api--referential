from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import MEDIUMINT, BIGINT
from sqlalchemy import (
    JSON,
    Column,
    Boolean,
    DateTime,
    ForeignKey
)

#
class DeliveryPointModel(EntityMeta):
    __tablename__ = "delivery_points"

    id = Column(MEDIUMINT(unsigned=True), primary_key=True, index=True)
    delivery_point_number = Column(BIGINT(unsigned=True), index=True, unique=True, nullable=False)
    area_id = Column(MEDIUMINT(unsigned=True), ForeignKey("areas.id"), nullable=False)
    pole_id = Column(MEDIUMINT(unsigned=True), ForeignKey("connection_poles.id"), nullable=False)
    infos = Column(JSON, nullable=True)
    connection_poles = Column(JSON, nullable=True)
    is_activated = Column(Boolean, index=True, default=True)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    area = relationship("AreaModel", back_populates="delivery_points")
    connection_pole = relationship("ConnectionPoleModel", back_populates="delivery_points")