from datetime import datetime
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import MEDIUMINT
from sqlalchemy import (
    Column,
    DateTime,
    Date,
    JSON,
    String,
)

class MeterDeliveryPointModel(EntityMeta):
    __tablename__ = "meter_delivery_points"

    id = Column(MEDIUMINT(unsigned=True), primary_key=True, index=True)
    meter_number = Column(String(15), index=True, unique=True, nullable=False)
    delivery_point_number = Column(String(15), index=True, unique=True, nullable=False)
    installation_date = Column(Date, nullable=False)
    infos = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)