from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.salesfinancial.models.TrackingTypeModel import (
    TrackingTypeModel,
)
from api.salesfinancial.schemas.TrackingTypeSchema import (
    CreateTrackingType,
)


class TrackingTypeRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        return self.db.query(
            func.max(TrackingTypeModel.code)
        ).one()[0]

    # get all tracking types function
    def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[TrackingTypeModel]:
        return (
            self.db.query(TrackingTypeModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

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
            .where(
                func.lower(TrackingTypeModel.name)
                == name.lower()
            )
            .first()
        )

    # create tracking type function
    def create(
        self, data: List[CreateTrackingType]
    ) -> List[CreateTrackingType]:
        self.db.execute(
            insert(TrackingTypeModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update tracking type function
    def update(
        self, data: TrackingTypeModel
    ) -> TrackingTypeModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete tracking type function
    def delete(self, tracking: TrackingTypeModel) -> None:
        self.db.delete(tracking)
        self.db.commit()
