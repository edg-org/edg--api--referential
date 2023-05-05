from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, MEDIUMINT
from sqlalchemy import (Column, JSON, String, Boolean, DateTime, ForeignKey)

class CityModel(EntityMeta):
    __tablename__ = "cities"

    id = Column(SMALLINT(unsigned=True), primary_key=True, index=True)
    code = Column(MEDIUMINT(unsigned=True), index=True, unique=True, nullable=False)
    prefecture_id = Column(TINYINT(unsigned=True), ForeignKey("prefectures.id"), nullable=False)
    level_id = Column(TINYINT(unsigned=True), ForeignKey("city_levels.id"), nullable=False)
    type_id = Column(TINYINT(unsigned=True), ForeignKey("city_types.id"), nullable=False)
    zipcode = Column(String(5), index=True, unique=True, nullable=False)
    infos = Column(JSON, nullable=False)
    is_activated = Column(Boolean, index=True, default=True)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    prefecture = relationship("PrefectureModel", back_populates="cities")
    city_type = relationship("CityTypeModel", back_populates="cities")
    city_level = relationship("CityLevelModel", back_populates="cities")
    
    areas = relationship("AreaModel", back_populates="city")