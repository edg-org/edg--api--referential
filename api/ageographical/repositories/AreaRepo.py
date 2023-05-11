from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.ageographical.models.AreaModel import AreaModel
from api.ageographical.schemas.AreaSchema import CreateArea

#
class AreaRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max id of area by city
    def maxcodebycity(self, city_code: int) -> int:
        codemax = (
            self.db.query(func.max(AreaModel.code))
            .where(AreaModel.infos["city_code"] == city_code)
            .one()[0]
        )
        return 0 if codemax is None else codemax

    # count total rows of area by name
    def countbyname(self, name: str) -> int:
        return self.db.query(AreaModel).where(
            func.lower(
                func.json_unquote(AreaModel.infos["name"])
            ) == name.lower()
        ).count()
    
    # count total rows of area by code
    def countbycode(self, code: int) -> int:
        return (
            self.db.query(AreaModel)
            .where(AreaModel.code == code)
            .count()
        )

    # get area id by code function
    def getidbycode(self, code: int) -> AreaModel:
        return (
            self.db.query(AreaModel.id)
            .where(AreaModel.code == code)
            .one()[0]
        )

    # get all areas function
    def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[AreaModel]:
        return (
            self.db.query(AreaModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get area by id function
    def get(self, id: int) -> AreaModel:
        return (
            self.db.query(AreaModel)
            .where(
                AreaModel.id == id
            ).first()
        )

    # get area id by code function
    def getidbycode(self, code: int) -> AreaModel:
        return (
            self.db.query(AreaModel.id)
            .where(
                AreaModel.code == code
            ).one()[0]
        )

    # get area code function
    def getbycode(self, code: str) -> AreaModel:
        return (
            self.db.query(AreaModel)
            .where(
                AreaModel.code == code
            ).first()
        )

    # get area name function
    def getbyname(self, name: str) -> AreaModel:
        return (
            self.db.query(AreaModel)
            .where(
                func.lower(
                    func.json_unquote(AreaModel.infos["name"])
                ) == name.lower()
            ).first()
        )

    # create area function
    def create(self, data: List[CreateArea]) -> List[CreateArea]:
        self.db.execute(
            insert(AreaModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update area function
    def update(self, data: CreateArea) -> AreaModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete area function
    def delete(self, area: AreaModel) -> None:
        self.db.delete(area)
        self.db.commit()
