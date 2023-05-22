from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.salesfinancial.models.HousingTypeModel import HousingTypeModel
from api.salesfinancial.schemas.HousingTypeSchema import CreateHousingType


class HousingTypeRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get all housing types function
    def list(self, skip: int = 0, limit: int = 100) -> List[HousingTypeModel]:
        return (
            self.db.query(HousingTypeModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get housing type by id function
    def get(self, id: int) -> HousingTypeModel:
        return (
            self.db.query(HousingTypeModel)
            .where(HousingTypeModel.id == id)
            .first()
        )

    # get housing type code function
    def getbycode(self, code: int) -> HousingTypeModel:
        return (
            self.db.query(HousingTypeModel)
            .where(HousingTypeModel.code == code)
            .first()
        )

    # get housing type name function
    def getbyname(self, name: str) -> HousingTypeModel:
        return (
            self.db.query(HousingTypeModel)
            .where(func.lower(HousingTypeModel.name) == name.lower())
            .first()
        )

    # get housing type id by name function
    def getidbyname(self, name: str) -> HousingTypeModel:
        return (
            self.db.query(HousingTypeModel.id)
            .where(func.lower(HousingTypeModel.name) == name.lower())
            .one()[0]
        )

    # create housing type function
    def create(self, data: List[CreateHousingType]) -> List[CreateHousingType]:
        self.db.execute(
            insert(HousingTypeModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update housing type function
    def update(self, data: CreateHousingType) -> HousingTypeModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete housing type function
    def delete(self, housing: HousingTypeModel) -> None:
        self.db.delete(housing)
        self.db.commit()
