from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.electrical.models.SupplyLineTypeModel import SupplyLineTypeModel
from api.electrical.schemas.SupplyLineTypeSchema import CreateSupplyLineType

class SupplyLineTypeRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        return self.db.query(
            func.max(SupplyLineTypeModel.code)
        ).one()[0]

    # get all supply line types function
    def list(self, skip: int = 0, limit: int = 100) -> List[SupplyLineTypeModel]:
        return (
            self.db.query(SupplyLineTypeModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get supply line type by id function
    def get(self, id: int) -> SupplyLineTypeModel:
        return (
            self.db.query(SupplyLineTypeModel)
            .where(SupplyLineTypeModel.id == id)
            .first()
        )

    # get supply line type code function
    def getbycode(self, code: str) -> SupplyLineTypeModel:
        return (
            self.db.query(SupplyLineTypeModel)
            .where(SupplyLineTypeModel.code == code)
            .first()
        )

    # get supply line type name function
    def getbyname(self, name: str) -> SupplyLineTypeModel:
        return (
            self.db.query(SupplyLineTypeModel)
            .where(
                func.lower(SupplyLineTypeModel.name) == name.lower()
            ).first()
        )

    # create supply line type function
    def create(self, data: List[CreateSupplyLineType]) -> List[CreateSupplyLineType]:
        self.db.execute(
            insert(SupplyLineTypeModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update supply line type function
    def update(self, data: CreateSupplyLineType) -> SupplyLineTypeModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete supply line type function
    def delete(self, supplyline: SupplyLineTypeModel) -> None:
        self.db.delete(supplyline)
        self.db.commit()
