from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.egeographical.models.CityModel import CityModel
from api.egeographical.schemas.CitySchema import CreateCity


class CityRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code of city by prefecture
    def maxcodebyzone(self, prefecture_code: int) -> int:
        return (
            self.db.query(func.max(CityModel.code))
            .where(
                CityModel.infos["prefecture_code"]
                == prefecture_code
            )
            .one()[0]
        )

    # get max zipcode of city by prefecture
    def maxzipcode_byzone(
        self, prefecture_code: int
    ) -> int:
        return (
            self.db.query(func.max(CityModel.zipcode))
            .where(
                CityModel.infos["prefecture_code"]
                == prefecture_code
            )
            .one()[0]
        )

    # get prefecture code by code function
    def getid_bycode(self, code: int) -> CityModel:
        return (
            self.db.query(CityModel.id)
            .where(CityModel.code == code)
            .one()[0]
        )

    # get all cities function
    def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[CityModel]:
        return (
            self.db.query(CityModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get city by id function
    def get(self, id: int) -> CityModel:
        return (
            self.db.query(CityModel)
            .where(CityModel.id == id)
            .first()
        )

    # get city code function
    def getbycode(self, code: str) -> CityModel:
        return (
            self.db.query(CityModel)
            .where(CityModel.code == code)
            .first()
        )

    # get city name function
    def getbyname(self, name: str) -> CityModel:
        return (
            self.db.query(CityModel)
            .where(
                func.lower(CityModel.infos["name"])
                == name.lower()
            )
            .first()
        )

    # get city code function
    def getbyzipcode(self, zipcode: str) -> CityModel:
        return (
            self.db.query(CityModel)
            .where(CityModel.zipcode == zipcode)
            .first()
        )

    # create city function
    def create(
        self, data: List[CreateCity]
    ) -> List[CreateCity]:
        self.db.execute(
            insert(CityModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update city function
    def update(self, data: CityModel) -> CityModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete city function
    def delete(self, city: CityModel) -> None:
        self.db.delete(city)
        self.db.commit()
