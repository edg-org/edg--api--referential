from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, PrimaryKeyConstraint, JSON, null, DateTime, Date
from sqlalchemy.orm import relationship
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from api.models.BaseModel import EntityMeta

from datetime import datetime
from sqlalchemy.sql import func

# from api.models.BookAuthorAssociation import (    book_author_association,)

#class Base(DeclarativeBase):
#    pass

class Logs(EntityMeta):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)

    # microservice: Mapped[str] = mapped_column(String(100), nullable = True)
    # endpoint: Mapped[str] = mapped_column(String(100), nullable = True)
    # user_uid: Mapped[str] = mapped_column(String(100), nullable = True)
    # user_email: Mapped[str] = mapped_column(String(100), nullable = True)
    # verb: Mapped[str] = mapped_column(String(100))

    # user = mapped_column(JSON, nullable = True, default = null()) 
    # prev_data = mapped_column(JSON, nullable = True, default = null())
    # data = mapped_column(JSON, nullable = True, default = null()) 

    # micro_service_uid: Mapped[str] = mapped_column(ForeignKey("ref_micro_services.unique_id")) 
    # micro_service_id: Mapped[int] = mapped_column(ForeignKey("ref_micro_services.id"))

    object_id: Mapped[str] = mapped_column(String(100), nullable = True) # nom de table de la DB
    micro_service_uid: Mapped[str] = mapped_column(String(50), nullable = True)
    infos = mapped_column(JSON, nullable = True, default = null()) 

    is_activated: Mapped[bool] = mapped_column(Boolean, nullable = True, default = True)         
    unique_id: Mapped[str] = mapped_column(String(50), nullable = False) 
    created_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now()) 
    updated_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now()) 
    deleted_at: Mapped[datetime] = mapped_column(nullable = True, default = func.now())     

    def __repr__(self) -> str:
        return f"Logs(id={self.id!r}, infos={self.infos!r})"

    def normalize(self):
        return {
            "id": self.id.__str__(),
            # "name": self.name.__str__(),
            # "infos": self.infos.__str__(), 
        }

    
# from sqlalchemy import Column, String
# from sqlalchemy.dialects.postgresql import UUID
# import uuid

# class MyTable(Base):
#     __tablename__ = 'mytable'
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = Column(String)

