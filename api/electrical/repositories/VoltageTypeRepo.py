from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.electrical.models.VoltageTypeModel import VoltageTypeModel
from api.electrical.schemas.VoltageTypeSchema import CreateVoltageType

class VoltageTypeRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get all voltage types function
    def list(self, skip: int = 0, limit: int = 100) -> List[VoltageTypeModel]:
        return (
            self.db.query(VoltageTypeModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get voltage type by id function
    def get(self, id: int) -> VoltageTypeModel:
        return (
            self.db.query(VoltageTypeModel)
            .where(VoltageTypeModel.id == id)
            .first()
        )

    # get voltage type code function
    def getbycode(self, code: str) -> VoltageTypeModel:
        return (
            self.db.query(VoltageTypeModel)
            .where(VoltageTypeModel.code == code)
            .first()
        )

    # get voltage type name function
    def getbyname(self, name: str) -> VoltageTypeModel:
        return (
            self.db.query(VoltageTypeModel)
            .where(
                func.lower(VoltageTypeModel.name) == name.lower()
            ).first()
        )

    # get voltage type short name function
    def getbyshortname(self, shortname: str) -> VoltageTypeModel:
        return (
            self.db.query(VoltageTypeModel)
            .where(
                func.lower(VoltageTypeModel.shortname) == shortname.lower()
            ).first()
        )

    # create voltage type function
    def create(self, data: List[CreateVoltageType]) -> List[CreateVoltageType]:
        self.db.execute(
            insert(VoltageTypeModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update voltage type function
    def update(self, data: CreateVoltageType) -> VoltageTypeModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete voltage type function
    def delete(self, supplyline: VoltageTypeModel) -> None:
        self.db.delete(supplyline)
        self.db.commit()