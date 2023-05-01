from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, PrimaryKeyConstraint, JSON, null, Text
from sqlalchemy.orm import relationship
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from api.models.BaseModel import EntityMeta
from datetime import datetime
from sqlalchemy.sql import func


class RefCityLevels(EntityMeta):
    __tablename__ = "ref_city_levels"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    is_activated: Mapped[bool] = mapped_column(Boolean, nullable = True, default = True) 
    infos = Column(Text, nullable = True)
    unique_id: Mapped[str] = mapped_column(String(50), nullable = False)

    # areas: Mapped[List["RefAreas"]] = relationship(back_populates = "type_areas")

    created_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now()) 
    updated_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now()) 
    deleted_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now())     

    def __repr__(self) -> str:
        return f"RefCityLevels(id={self.id!r}, infos={self.infos!r})"

    def normalize(self):
        return {
            "id": self.id.__str__(), 
            "name": self.name.__str__(),
            # "infos": self.infos.__str__(),
        }

