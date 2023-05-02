from datetime import datetime
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import MEDIUMINT
from sqlalchemy import (Column, DateTime, Date, JSON, UniqueConstraint, ForeignKey)

class MeterDeliveryPointModel(EntityMeta):
    __tablename__ = "meter_delivery_points"

    id = Column(MEDIUMINT(unsigned=True), primary_key=True, index=True)
    meter_id = Column(MEDIUMINT(unsigned=True), ForeignKey("electric_meters.id"), nullable=False)
    delivery_point_id = Column(MEDIUMINT(unsigned=True), index=True, unique=True, nullable=False)
    installation_date = Column(Date, nullable=False)
    infos = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=datetime.utcnow().isoformat(), nullable=False)
    UniqueConstraint("meter_id", name="uix1_mdp")
    UniqueConstraint("delivery_point_id", name="uix2_mdp")