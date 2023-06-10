from typing import List
from sqlalchemy import insert
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.logs.models.LogModel import LogModel
from api.logs.schemas.LogSchema import CreateLog

class LogRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get all area types function
    def list(self, skip: int = 0, limit: int = 100) -> List[LogModel]:
        return self.db.query(LogModel).offset(skip).limit(limit).all()

    # get area type by id function
    def get(self, id: int) -> LogModel:
        return self.db.query(LogModel).where(LogModel.id == id).first()
    
    # create area type function
    def create(self, data: List[CreateLog]) -> List[CreateLog]:
        self.db.execute(insert(LogModel), encoders.jsonable_encoder(data))
        self.db.commit()
        return data