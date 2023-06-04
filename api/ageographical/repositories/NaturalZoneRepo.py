from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from sqlalchemy import insert, func, update
from api.ageographical.models.NaturalZoneModel import ZoneModel
from api.ageographical.schemas.NaturalZoneSchema import CreateZone, ZoneUpdate

#
class ZoneRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # count total rows of natural region
    def countrows(self) -> int:
        return self.db.query(ZoneModel).count()

    # get max code of natural region
    def maxcode(self) -> int:
        codemax = self.db.query(
            func.max(ZoneModel.code)
        ).one()[0]
        return 0 if codemax is None else codemax

    # get all regions function
    def list(self, skip: int = 0, limit: int = 100) -> List[ZoneModel]:
        return (
            self.db.query(ZoneModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get region by id function
    def get(self, id: int) -> ZoneModel:
        return (
            self.db.query(ZoneModel)
            .where(ZoneModel.id == id)
            .first()
        )

    # get region id by code function
    def getidbycode(self, code: int) -> ZoneModel:
        return (
            self.db.query(ZoneModel.id)
            .where(ZoneModel.code == code)
            .one()[0]
        )

     # get region id by name function
    def getidbyname(self, name: str) -> ZoneModel:
        return (
            self.db.query(ZoneModel.id)
            .where(func.lower(ZoneModel.name) == name.lower())
            .one()[0]
        )

    # get region by code function
    def getbycode(self, code: int) -> ZoneModel:
        return (
            self.db.query(ZoneModel)
            .where(ZoneModel.code == code)
            .first()
        )

    # get region by name function
    def getbyname(self, name: str) -> ZoneModel:
        return (
            self.db.query(ZoneModel)
            .where(
                func.lower(ZoneModel.name) == name.lower()
            )
            .first()
        )
        
    # count total rows of transformer by code
    def countbycode(self, code: str) -> int:
        return (
            self.db.query(ZoneModel)
            .where(ZoneModel.code == code)
            .count()
        )

    # create region function
    def create(self, data: List[CreateZone]) -> List[CreateZone]:
        self.db.execute(
            insert(ZoneModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update region function
    def update(self,code: int, data: dict) -> ZoneModel:
        self.db.execute(
            update(ZoneModel)
            .where(ZoneModel.code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=code)

    # delete region function
    def delete(self, region: ZoneModel) -> None:
        self.db.delete(region)
        self.db.commit()
