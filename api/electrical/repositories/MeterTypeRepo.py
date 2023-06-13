from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from sqlalchemy import insert, func, update
from api.electrical.models.MeterTypeModel import MeterTypeModel
from api.electrical.schemas.MeterTypeSchema import CreateMeterType

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
    def list(self, skip: int = 0, limit: int = 100) -> List[MeterTypeModel]:
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
    def getbycode(self, code: int) -> MeterTypeModel:
        return (
            self.db.query(MeterTypeModel)
            .where(MeterTypeModel.code == code)
            .first()
        )

    # get meter type name function
    def getbyname(self, name: str) -> MeterTypeModel:
        return (
            self.db.query(MeterTypeModel)
            .where(func.lower(MeterTypeModel.name) == name.lower())
            .first()
        )

    # create meter type function
    def create(self, data: List[CreateMeterType]) -> List[CreateMeterType]:
        self.db.execute(
            insert(MeterTypeModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update meter type function
    def update(self, code: int, data: dict) -> MeterTypeModel:
        self.db.execute(
            update(MeterTypeModel)
            .where(MeterTypeModel.code == code)
            .values(**data)
        )
        self.db.commit()

        return self.getbycode(code=data['code'])

    # delete meter type function
    def delete(self, type: MeterTypeModel) -> None:
        self.db.delete(type)
        self.db.commit()
