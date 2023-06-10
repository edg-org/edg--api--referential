from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, MEDIUMINT
from sqlalchemy import (
    JSON,
    String,
    Column,
    Boolean,
    DateTime,
    ForeignKey
)

#
class TransformerModel(EntityMeta):
    __tablename__ = "transformers"

    id = Column(MEDIUMINT(unsigned=True), primary_key=True, index=True)
    transformer_code = Column(String(15), index=True, unique=True, nullable=False)
    infos = Column(JSON, nullable=False)
    area_id = Column(MEDIUMINT(unsigned=True), ForeignKey("areas.id"), nullable=True)
    fixation_type_id = Column(TINYINT(unsigned=True), ForeignKey("fixation_types.id"), nullable=True)
    is_activated = Column(Boolean, index=True, default=True)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow().isoformat(), nullable=True)

    area = relationship("AreaModel", back_populates="transformers")
    fixation_type = relationship("FixationTypeModel", back_populates="transformers")
    
    connection_poles = relationship("ConnectionPoleModel", back_populates="transformer")