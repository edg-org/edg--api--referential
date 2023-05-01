from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, PrimaryKeyConstraint, JSON, null
from sqlalchemy.orm import relationship
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from api.models.BaseModel import EntityMeta
from datetime import datetime
from sqlalchemy.sql import func

from api.models.RefNaturalRegionsModel import RefNaturalRegions
from api.models.RefPrefecturesModel import RefPrefectures

class RefAreas(EntityMeta):
    __tablename__ = "ref_areas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    code: Mapped[int] = mapped_column(nullable = False, unique = True)
    is_activated: Mapped[bool] = mapped_column(Boolean, nullable = True, default = True) 
    infos = mapped_column(JSON, nullable = True, default = null()) 
    unique_id: Mapped[str] = mapped_column(String(50), nullable = False) 

    cities_id: Mapped[int] = mapped_column(ForeignKey("ref_cities.id"))
    type_areas_id: Mapped[int] = mapped_column(ForeignKey("ref_type_areas.id"))

    cities: Mapped["RefCities"] = relationship(back_populates = "areas")
    type_areas: Mapped["RefTypeAreas"] = relationship(back_populates = "areas")
    agencies: Mapped[List["RefAgencies"]] = relationship(back_populates = "areas")

    created_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now()) 
    updated_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now()) 
    deleted_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now())     

    def __repr__(self) -> str:
        return f"RefAreas(id={self.id!r}, infos={self.infos!r})"

    def normalize(self):
        return {
            "id": self.id.__str__(),
            # "name": self.name.__str__(),
            # "infos": self.infos.__str__(),
        }

