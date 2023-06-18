from datetime import datetime
from sqlalchemy import String
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT
#from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, DateTime, String

class HousingTypeModel(EntityMeta):
    
    __tablename__ = "housing_types"

    id = Column(TINYINT(unsigned=True), primary_key=True, index=True)
    code = Column(TINYINT(unsigned=True), index=True, unique=True, nullable=False)
    name = Column(String(45), index=True, unique=True, nullable=False)
    shortname = Column(String(5), index=True, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)