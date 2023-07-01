from datetime import datetime
from sqlalchemy import String
from api.configs.BaseModel import EntityMeta
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, mapped_column
#from sqlalchemy import Column, DateTime, String

class HousingTypeModel(EntityMeta):
    __tablename__ = "housing_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int] = mapped_column(TINYINT(unsigned=True), index=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(45), index=True, unique=True, nullable=False)
    shortname: Mapped[str] = mapped_column(String(5), index=True, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=datetime.utcnow().isoformat(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.utcnow().isoformat(), nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(nullable=True)