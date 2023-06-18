from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from sqlalchemy import insert, func, update
from api.electrical.models.FixationTypeModel import FixationTypeModel
from api.electrical.schemas.FixationTypeSchema import CreateFixationType

class FixationTypeRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get all fixation types function
    def list(self, start: int = 0, size: int = 100) -> List[FixationTypeModel]:
        return (
            self.db.query(FixationTypeModel)
            .offset(start)
            .limit(size)
            .all()
        )

    # get fixation type by id function
    def get(self, id: int) -> FixationTypeModel:
        return (
            self.db.query(FixationTypeModel)
            .where(FixationTypeModel.id == id)
            .first()
        )

    # get fixation type code function
    def getbycode(self, code: str) -> FixationTypeModel:
        return (
            self.db.query(FixationTypeModel)
            .where(FixationTypeModel.code == code)
            .first()
        )

    # get fixation type name function
    def getbyname(self, name: str) -> FixationTypeModel:
        return (
            self.db.query(FixationTypeModel)
            .where(func.lower(FixationTypeModel.name) == name.lower())
            .first()
        )

    # create fixation type function
    def create(self, data: List[CreateFixationType]) -> List[CreateFixationType]:
        self.db.execute(
            insert(FixationTypeModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update fixation type function
    def update(self, code: int, data: dict) -> FixationTypeModel:
        self.db.execute(
            update(FixationTypeModel)
            .where(FixationTypeModel.code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=code)

    # delete fixation type function
    def delete(self, supplyline: FixationTypeModel) -> None:
        self.db.delete(supplyline)
        self.db.commit()