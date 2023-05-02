from datetime import datetime
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import (Column, DateTime, JSON)

class LoggerModel(EntityMeta):
    __tablename__ = "logger"

    id = Column(TINYINT(unsigned=True), primary_key=True, index=True)
    infos = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)