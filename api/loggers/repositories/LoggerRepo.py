from typing import List
from sqlalchemy import insert
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.loggers.models.LoggerModel import LoggerModel
from api.loggers.schemas.LoggerSchema import CreateLogger

class LoggerRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get all area types function
    def list(self, skip: int = 0, limit: int = 100) -> List[LoggerModel]:
        return self.db.query(LoggerModel).offset(skip).limit(limit).all()

    # get area type by id function
    def get(self, id: int) -> LoggerModel:
        return self.db.query(LoggerModel).where(LoggerModel.id == id).first()
    
    # create area type function
    def create(self, data: List[CreateLogger]) -> List[CreateLogger]:
        self.db.execute(insert(LoggerModel), encoders.jsonable_encoder(data))
        self.db.commit()
        return data