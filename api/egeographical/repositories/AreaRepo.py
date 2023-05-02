from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.egeographical.models.AreaModel import AreaModel
from api.egeographical.schemas.AreaSchema import CreateArea


class AreaRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max id of area by city
    def maxcode_bycity(self, city_code: int) -> int:
        return (
            self.db.query(func.max(AreaModel.code))
            .where(
                AreaModel.infos["city_code"] == city_code
            )
            .one()[0]
        )

    # get area id by code function
    def getid_bycode(self, code: int) -> AreaModel:
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
            .where(AreaModel.id == id)
            .first()
        )

    # get area code function
    def getbycode(self, code: str) -> AreaModel:
        return (
            self.db.query(AreaModel)
            .where(AreaModel.code == code)
            .first()
        )

    # get area name function
    def getbyname(self, name: str) -> AreaModel:
        return (
            self.db.query(AreaModel)
            .where(AreaModel.infos["name"] == name)
            .first()
        )

    # create area function
    def create(
        self, data: List[CreateArea]
    ) -> List[CreateArea]:
        self.db.execute(
            insert(AreaModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update area function
    def update(self, data: AreaModel) -> AreaModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete area function
    def delete(self, area: AreaModel) -> None:
        self.db.delete(area)
        self.db.commit()
