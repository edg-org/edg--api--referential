from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from sqlalchemy import insert, func, update
from api.salesfinancial.models.TrackingTypeModel import TrackingTypeModel
from api.salesfinancial.schemas.TrackingTypeSchema import CreateTrackingType


class TrackingTypeRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        codemax = self.db.query(func.max(TrackingTypeModel.code)).one()[0]
        return 0 if codemax is None else codemax

    # get all tracking types function
    def list(self, start: int = 0, size: int = 100) -> List[TrackingTypeModel]:
        query = self.db.query(TrackingTypeModel)
        return query.offset(start).limit(size).all()

    # get tracking type by id function
    def get(self, id: int) -> TrackingTypeModel:
        return (
            self.db.query(TrackingTypeModel)
            .where(TrackingTypeModel.id == id)
            .first()
        )

    # get tracking type code function
    def getbycode(self, code: str) -> TrackingTypeModel:
        return (
            self.db.query(TrackingTypeModel)
            .where(TrackingTypeModel.code == code)
            .first()
        )

    # get tracking type name function
    def getbyname(self, name: str) -> TrackingTypeModel:
        return (
            self.db.query(TrackingTypeModel)
            .where(func.lower(TrackingTypeModel.name) == name.lower())
            .first()
        )

    # get tracking type id by name function
    def getidbyname(self, name: str) -> TrackingTypeModel:
        return (
            self.db.query(TrackingTypeModel.id)
            .where(func.lower(TrackingTypeModel.name) == name.lower())
            .one()[0]
        )

    # create tracking type function
    def create(self, data: List[CreateTrackingType]) -> List[CreateTrackingType]:
        self.db.execute(
            insert(TrackingTypeModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update tracking type function
    def update(self, code: int, data: dict) -> TrackingTypeModel:
        self.db.execute(
            update(TrackingTypeModel)
            .where(TrackingTypeModel.code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=code)

    # delete tracking type function
    def delete(self, tracking: TrackingTypeModel) -> None:
        self.db.delete(tracking)
        self.db.commit()
