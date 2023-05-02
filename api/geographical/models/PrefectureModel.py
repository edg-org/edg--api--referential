from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT, MEDIUMINT
from sqlalchemy import (Column, JSON, String, Boolean, DateTime, ForeignKey)

class PrefectureModel(EntityMeta):
    __tablename__ = "prefectures"

    id = Column(TINYINT(unsigned=True), primary_key=True, index=True)
    code = Column(MEDIUMINT(unsigned=True), index=True, unique=True, nullable=False)
    prefecture_number = Column(String(2), index=True, unique=True, nullable=False)
    region_id = Column(TINYINT(unsigned=True), ForeignKey("regions.id"), nullable=False)
    infos = Column(JSON, nullable=False)
    is_capital = Column(Boolean, index=True, default=True)
    is_activated = Column(Boolean, index=True, default=True)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    region = relationship("RegionModel", back_populates="prefectures")
    cities = relationship("CityModel", back_populates="prefecture")