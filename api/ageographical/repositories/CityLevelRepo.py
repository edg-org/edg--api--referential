from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from sqlalchemy import insert, update, func
from api.ageographical.models.CityLevelModel import CityLevelModel
from api.ageographical.schemas.CityLevelSchema import CreateCityLevel, CityLevelUpdate

#
class CityLevelRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        codemax = (
            self.db.query(func.max(CityLevelModel.code))
            .one()[0]
        )
        return 0 if codemax is None else codemax

    # get all city levels function
    def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[CityLevelModel]:
        return (
            self.db.query(CityLevelModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get city level by id function
    def get(self, id: int) -> CityLevelModel:
        return (
            self.db.query(CityLevelModel)
            .where(CityLevelModel.id == id)
            .first()
        )

    # get city level code function
    def getbycode(self, code: str) -> CityLevelModel:
        return (
            self.db.query(CityLevelModel)
            .where(CityLevelModel.code == code)
            .first()
        )

    # get city level name function
    def getbyname(self, name: str) -> CityLevelModel:
        return (
            self.db.query(CityLevelModel)
            .where(func.lower(CityLevelModel.name) == name.lower())
            .first()
        )

    # create city level function
    def create(self, data: List[CreateCityLevel]) -> List[CreateCityLevel]:
        self.db.execute(
            insert(CityLevelModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update city level function
    def update(self, code: int, data: dict) -> CityLevelModel:
        self.db.execute(
            update(CityLevelUpdate)
            .where(CityLevelUpdate.code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=code)

    # delete city level function
    def delete(self, city: CityLevelModel) -> None:
        self.db.delete(city)
        self.db.commit()
