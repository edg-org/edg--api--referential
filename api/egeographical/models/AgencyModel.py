from datetime import datetime
from sqlalchemy.orm import relationship
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT, MEDIUMINT
from sqlalchemy import (
    Column,
    JSON,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
)


class AgencyModel(EntityMeta):
    __tablename__ = "agencies"

    id = Column(
        MEDIUMINT(unsigned=True),
        primary_key=True,
        index=True,
    )
    code = Column(
        Integer, index=True, unique=True, nullable=False
    )
    area_id = Column(
        MEDIUMINT(unsigned=True),
        ForeignKey("areas.id"),
        nullable=False,
    )
    infos = Column(JSON, nullable=False)
    is_activated = Column(Boolean, index=True, default=True)
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
    deleted_at = Column(
        DateTime(timezone=True), nullable=True
    )

    area = relationship(
        "AreaModel", back_populates="agencies"
    )
