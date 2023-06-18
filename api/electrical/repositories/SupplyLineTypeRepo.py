from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from sqlalchemy import insert, func, update
from api.electrical.models.SupplyLineTypeModel import SupplyLineTypeModel
from api.electrical.schemas.SupplyLineTypeSchema import CreateSupplyLineType

class SupplyLineTypeRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get all supply line types function
    def list(self, start: int = 0, size: int = 100) -> List[SupplyLineTypeModel]:
        return (
            self.db.query(SupplyLineTypeModel)
            .offset(start)
            .limit(size)
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
    def update(self, code: int, data: dict) -> SupplyLineTypeModel:
        self.db.execute(
            update(SupplyLineTypeModel)
            .where(SupplyLineTypeModel.code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=code)

    # delete supply line type function
    def delete(self, supplyline: SupplyLineTypeModel) -> None:
        self.db.delete(supplyline)
        self.db.commit()