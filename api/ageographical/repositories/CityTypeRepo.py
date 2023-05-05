from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.ageographical.models.CityTypeModel import CityTypeModel
from api.ageographical.schemas.CityTypeSchema import CreateCityType

#
class CityTypeRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code of city type
    def maxcode(self) -> int:
        return self.db.query(
            func.max(CityTypeModel.code)
        ).one()[0]

    # get all city types function
    def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[CityTypeModel]:
        return (
            self.db.query(CityTypeModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get city type by id function
    def get(self, id: int) -> CityTypeModel:
        return (
            self.db.query(CityTypeModel)
            .where(CityTypeModel.id == id)
            .first()
        )

    # get city type code function
    def getbycode(self, code: str) -> CityTypeModel:
        return (
            self.db.query(CityTypeModel)
            .where(CityTypeModel.code == code)
            .first()
        )

    # get city type name function
    def getbyname(self, name: str) -> CityTypeModel:
        return (
            self.db.query(CityTypeModel)
            .where(
                func.lower(CityTypeModel.name)
                == name.lower()
            )
            .first()
        )

    # create city type function
    def create(
        self, data: List[CreateCityType]
    ) -> List[CreateCityType]:
        self.db.execute(
            insert(CityTypeModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update city type function
    def update(self, data: CityTypeModel) -> CityTypeModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete city type function
    def delete(self, city: CityTypeModel) -> None:
        self.db.delete(city)
        self.db.commit()
