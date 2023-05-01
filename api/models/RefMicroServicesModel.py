from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, PrimaryKeyConstraint, JSON, null, DateTime, Date
from sqlalchemy.orm import relationship
from typing import List, Set, Tuple, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from api.models.BaseModel import EntityMeta

from datetime import datetime
from sqlalchemy.sql import func

class RefMicroServices(EntityMeta):
    __tablename__ = "ref_micro_services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    infos = mapped_column(JSON, nullable = True, default = null()) 
    
    is_activated: Mapped[bool] = mapped_column(Boolean, nullable = True, default = True) 
    unique_id: Mapped[str] = mapped_column(String(50), nullable = False) 
    created_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now()) 
    updated_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now()) 
    deleted_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now())     

    # adm_regions: Mapped[List["RefAdmRegions"]] = relationship(back_populates="natural_region")

    def __repr__(self) -> str:
        return f"RefMicroServices(id={self.id!r}, infos={self.infos!r})"

    def normalize(self):
        return {
            "id": self.id.__str__(),
            # "name": self.name.__str__(),
            # "infos": self.infos.__str__(), 
        }
