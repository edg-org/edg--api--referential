from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, PrimaryKeyConstraint, JSON, null
from sqlalchemy.orm import relationship
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from datetime import datetime
from sqlalchemy.sql import func

from api.models.BaseModel import EntityMeta
from api.models.RefNaturalRegionsModel import RefNaturalRegions

class RefAdmRegions(EntityMeta):
    __tablename__ = "ref_adm_regions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    code: Mapped[int] = mapped_column(nullable = False, unique = True)
    infos = mapped_column(JSON, nullable = True, default = null()) 

    natural_region_id: Mapped[int] = mapped_column(ForeignKey("ref_natural_regions.id"))
    natural_region: Mapped["RefNaturalRegions"] = relationship(back_populates = "adm_regions")

    prefectures: Mapped[List["RefPrefectures"]] = relationship(back_populates="adm_region")

    # adm_region_prefectures: Mapped[List["RefPrefectures"]] = relationship(back_populates="prefectures_adm_region", cascade="all, delete-orphan") 
    is_activated: Mapped[bool] = mapped_column(Boolean, nullable = True, default = True) 
    unique_id: Mapped[str] = mapped_column(String(50), nullable = False) 
    created_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now()) 
    updated_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now()) 
    deleted_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now())     

    def __repr__(self) -> str: 
        return f"RefAdmRegions(id={self.id!r}, infos={self.infos!r})"

    def normalize(self):
        return {
            "id": self.id.__str__(),
            # "infos": self.infos.__str__(),
        }