from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.egeographical.models.NaturalZoneModel import (
    ZoneModel,
)
from api.egeographical.schemas.NaturalZoneSchema import (
    CreateZone,
)


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
        return self.db.query(
            func.max(ZoneModel.code)
        ).one()[0]

    # get all regions function
    def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[ZoneModel]:
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
    def getid_bycode(self, code: int) -> ZoneModel:
        return (
            self.db.query(ZoneModel.id)
            .where(ZoneModel.code == code)
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

    # create region function
    def create(
        self, data: List[CreateZone]
    ) -> List[ZoneModel]:
        self.db.execute(
            insert(ZoneModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update region function
    def update(self, data: ZoneModel) -> ZoneModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete region function
    def delete(self, region: ZoneModel) -> None:
        self.db.delete(region)
        self.db.commit()
