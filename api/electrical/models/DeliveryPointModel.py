from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import MEDIUMINT
from sqlalchemy import (
    Column,
    DateTime,
    JSON,
    String,
    ForeignKey,
)


class DeliveryPointModel(EntityMeta):
    __tablename__ = "delivery_points"

    id = Column(MEDIUMINT(unsigned=True), primary_key=True, index=True)
    delivery_point_number = Column(String(15), index=True, unique=True, nullable=False)
    area_id = Column(MEDIUMINT(unsigned=True), ForeignKey("areas.id"), nullable=False)
    infos = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)

    area = relationship("AreaModel", back_populates="delivery_points")