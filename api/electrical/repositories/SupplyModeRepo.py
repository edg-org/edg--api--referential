from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from sqlalchemy import insert, func, update
from api.electrical.models.SupplyModeModel import SupplyModeModel
from api.electrical.schemas.SupplyModeSchema import CreateSupplyMode

class SupplyModeRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        return self.db.query(
            func.max(SupplyModeModel.code)
        ).one()[0]

    # get all supply modes function
    def list(self, skip: int = 0, limit: int = 100) -> List[SupplyModeModel]:
        return (
            self.db.query(SupplyModeModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get supply mode by id function
    def get(self, id: int) -> SupplyModeModel:
        return (
            self.db.query(SupplyModeModel)
            .where(SupplyModeModel.id == id)
            .first()
        )

    # get supply mode code function
    def getbycode(self, code: str) -> SupplyModeModel:
        return (
            self.db.query(SupplyModeModel)
            .where(SupplyModeModel.code == code)
            .first()
        )

    # get supply mode name function
    def getbyname(self, name: str) -> SupplyModeModel:
        return (
            self.db.query(SupplyModeModel)
            .where(func.lower(SupplyModeModel.name) == name.lower())
            .first()
        )

    # get supply mode id by name function
    def getidbyname(self, name: str) -> int:
        return (
            self.db.query(SupplyModeModel.id)
            .where(func.lower(SupplyModeModel.name) == name.lower())
            .one()[0]
        )
    
    # create supply mode function
    def create(self, data: List[CreateSupplyMode]) -> List[CreateSupplyMode]:
        self.db.execute(
            insert(SupplyModeModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update supply mode function
    def update(self, code: int, data: dict) -> SupplyModeModel:
        self.db.execute(
            update(SupplyModeModel)
            .where(SupplyModeModel.code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=data['code'])

    # delete supply mode function
    def delete(self, meter: SupplyModeModel) -> None:
        self.db.delete(meter)
        self.db.commit()
