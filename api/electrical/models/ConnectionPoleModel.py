from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import MEDIUMINT
from sqlalchemy import (
    Column,
    DateTime,
    JSON,
    String,
    Boolean,
    ForeignKey
)

#
class ConnectionPoleModel(EntityMeta):
    
    __tablename__ = "connection_poles"

    id = Column(MEDIUMINT(unsigned=True), primary_key=True, index=True)
    pole_number = Column(String(15), index=True, unique=True, nullable=False)
    infos = Column(JSON, nullable=False)
    area_id = Column(MEDIUMINT(unsigned=True), ForeignKey("areas.id"), nullable=False)
    transformer_id = Column(MEDIUMINT(unsigned=True), ForeignKey("transformers.id"), nullable=False)
    is_activated = Column(Boolean, index=True, default=True)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    area = relationship("AreaModel", back_populates="connection_poles")
    transformer = relationship("TransformerModel", back_populates="connection_poles")

    delivery_points = relationship("DeliveryPointModel", back_populates="connection_pole")