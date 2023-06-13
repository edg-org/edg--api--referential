from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import (Column, DateTime, String)

class CityTypeModel(EntityMeta):
    __tablename__ = "city_types"

    id = Column(TINYINT(unsigned=True), primary_key=True, index=True)
    code = Column(TINYINT(unsigned=True), index=True, unique=True, nullable=False)
    name = Column(String(50), index=True, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    cities = relationship("CityModel", back_populates="city_type")