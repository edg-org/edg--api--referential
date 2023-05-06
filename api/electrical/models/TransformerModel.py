from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT, MEDIUMINT
from sqlalchemy import (
    Column,
    DateTime,
    JSON,
    String,
    ForeignKey,
)


class TransformerModel(EntityMeta):
    __tablename__ = "transformers"

    id = Column(
        MEDIUMINT(unsigned=True),
        primary_key=True,
        index=True,
    )
    code = Column(
        String(5), index=True, unique=True, nullable=False
    )
    transformer_number = Column(
        String(15), index=True, unique=True, nullable=False
    )
    departure_id = Column(
        TINYINT(unsigned=True),
        ForeignKey("energy_departures.id"),
        nullable=False,
    )
    area_id = Column(
        MEDIUMINT(unsigned=True),
        ForeignKey("areas.id"),
        nullable=False,
    )
    infos = Column(JSON, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=datetime.utcnow().isoformat(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=datetime.utcnow().isoformat(),
        nullable=True,
    )

    area = relationship(
        "AreaModel", back_populates="transformers"
    )
    energy_departure = relationship(
        "EnergyDepartureModel",
        back_populates="transformers",
    )

    connection_points = relationship(
        "ConnectionPointModel", back_populates="transformer"
    )
