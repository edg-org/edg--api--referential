from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from sqlalchemy import (Column, JSON, Boolean, DateTime, ForeignKey)

class RegionModel(EntityMeta):
    __tablename__ = "regions"

    id = Column(TINYINT(unsigned=True), primary_key=True, index=True)
    code = Column(SMALLINT(unsigned=True), index=True, unique=True, nullable=False)
    zone_id = Column(TINYINT(unsigned=True), ForeignKey("natural_zones.id"), nullable=False)
    infos = Column(JSON, nullable=False)
    is_activated = Column(Boolean, index=True, default=True)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    zone = relationship("ZoneModel", back_populates="regions")
    prefectures = relationship("PrefectureModel", back_populates="region")