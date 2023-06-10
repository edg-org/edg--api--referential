from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import (Column, DateTime, JSON, String)

class VoltageTypeModel(EntityMeta):
    __tablename__ = "voltage_types"

    id = Column(TINYINT(unsigned=True), primary_key=True, index=True)
    code = Column(TINYINT(unsigned=True), index=True, unique=True, nullable=False)
    name = Column(String(50), index=True, unique=True, nullable=False)
    shortname = Column(String(15), index=True, unique=True, nullable=False)
    infos = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)
    
    energy_supply_lines = relationship("EnergySupplyLineModel", back_populates="voltage_type")