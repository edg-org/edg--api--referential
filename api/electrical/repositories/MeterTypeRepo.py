from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.electrical.models.MeterTypeModel import (
    MeterTypeModel,
)
from api.electrical.schemas.MeterTypeSchema import (
    CreateMeterType,
)


class MeterTypeRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        return self.db.query(
            func.max(MeterTypeModel.code)
        ).one()[0]

    # get all meter types function
    def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[MeterTypeModel]:
        return (
            self.db.query(MeterTypeModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get meter type by id function
    def get(self, id: int) -> MeterTypeModel:
        return (
            self.db.query(MeterTypeModel)
            .where(MeterTypeModel.id == id)
            .first()
        )

    # get meter type code function
    def getbycode(self, code: str) -> MeterTypeModel:
        return (
            self.db.query(MeterTypeModel)
            .where(MeterTypeModel.code == code)
            .first()
        )

    # get meter type name function
    def getbyname(self, name: str) -> MeterTypeModel:
        return (
            self.db.query(MeterTypeModel)
            .where(
                func.lower(MeterTypeModel.name)
                == name.lower()
            )
            .first()
        )

    # create meter type function
    def create(
        self, data: List[CreateMeterType]
    ) -> List[CreateMeterType]:
        self.db.execute(
            insert(MeterTypeModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update meter type function
    def update(
        self, data: MeterTypeModel
    ) -> MeterTypeModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete meter type function
    def delete(self, meter: MeterTypeModel) -> None:
        self.db.delete(meter)
        self.db.commit()
