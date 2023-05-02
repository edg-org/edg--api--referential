from datetime import datetime
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import MEDIUMINT
from sqlalchemy import (
    Column,
    DateTime,
    Date,
    String,
    UniqueConstraint,
)


class MeterDeliveryPointHistoryModel(EntityMeta):
    __tablename__ = "meter_delivery_point_histories"

    id = Column(
        MEDIUMINT(unsigned=True),
        primary_key=True,
        index=True,
    )
    meter_number = Column(
        String(15), index=True, unique=True, nullable=False
    )
    delivery_point_number = Column(
        String(15),
        index=True,
        unique=True,
        nullable=False,
    )
    installation_date = Column(Date, nullable=False)
    uninstallation_date = Column(Date, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=datetime.utcnow().isoformat(),
        nullable=False,
    )
    UniqueConstraint(
        "meter_number",
        "delivery_point_number",
        "installation_date",
        name="uix1_mdph",
    )
