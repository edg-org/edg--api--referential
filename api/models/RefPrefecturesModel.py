from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, PrimaryKeyConstraint, JSON, null
from sqlalchemy.orm import relationship
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from api.models.BaseModel import EntityMeta
from datetime import datetime
from sqlalchemy.sql import func

from api.models.RefNaturalRegionsModel import RefNaturalRegions

class RefPrefectures(EntityMeta):
    __tablename__ = "ref_prefectures" 

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    code: Mapped[int] = mapped_column(nullable = False, unique = True)
    infos = Column(JSON, nullable = True, default = null()) 

    region_id: Mapped[int] = mapped_column(ForeignKey("ref_adm_regions.id"))

    is_activated: Mapped[bool] = mapped_column(Boolean, nullable = True, default = True) 
    unique_id: Mapped[str] = mapped_column(String(50), nullable = False)  

    created_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now()) 
    updated_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now()) 
    deleted_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now())     

    adm_region: Mapped["RefAdmRegions"] = relationship(back_populates = "prefectures")
    cities: Mapped[List["RefCities"]] = relationship(back_populates = "prefectures")

    def __repr__(self) -> str:
        return f"RefPrefectures(id={self.id!r}, infos={self.infos!r})"

    def normalize(self):
        return {
            "id": self.id.__str__(),
            # "infos": self.infos.__str__(), 
        }

