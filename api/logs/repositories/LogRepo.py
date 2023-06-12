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
    def list(self, start: int = 0, size: int = 100) -> (int, List[LogModel]):
        query = self.db.query(LogModel)
        return query.count(), query.offset(start).limit(size).all()

    # get area type by id function
    def get(self, id: int) -> LogModel:
        return self.db.query(LogModel).where(LogModel.id == id).first()
    
    # create area type function
    def create(self, data: List[CreateLog]) -> List[CreateLog]:
        self.db.execute(
            insert(LogModel),
            encoders.jsonable_encoder(data)
        )
        self.db.commit()
        return data