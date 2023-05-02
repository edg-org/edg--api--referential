from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.egeographical.models.RegionModel import RegionModel
from api.egeographical.schemas.RegionSchema import (
    CreateRegion,
)


class RegionRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # count total rows of administative region by natural region
    def countrows_byzone(self, zone_code: int) -> int:
        return (
            self.db.query(RegionModel)
            .where(
                RegionModel.infos["zone_code"] == zone_code
            )
            .count()
        )

    # get max id of administrative region by natural region
    def maxcode_byzone(self, zone_code: int) -> int:
        return (
            self.db.query(func.max(RegionModel.code))
            .where(
                RegionModel.infos["zone_code"] == zone_code
            )
            .one()[0]
        )

    # get administrative region id by code function
    def getid_bycode(self, code: int) -> RegionModel:
        return (
            self.db.query(RegionModel.id)
            .where(RegionModel.code == code)
            .one()[0]
        )

    # get all regions function
    def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[RegionModel]:
        return (
            self.db.query(RegionModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get administative region by id function
    def get(self, id: int) -> RegionModel:
        return (
            self.db.query(RegionModel)
            .where(RegionModel.id == id)
            .first()
        )

    # get administative region code function
    def getbycode(self, code: str) -> RegionModel:
        return (
            self.db.query(RegionModel)
            .where(RegionModel.code == code)
            .first()
        )

    # get administative region name function
    def getbyname(self, name: str) -> RegionModel:
        return (
            self.db.query(RegionModel)
            .where(
                func.lower(RegionModel.infos["name"])
                == name.lower()
            )
            .first()
        )

    # create administative region function
    def create(
        self, data: List[CreateRegion]
    ) -> List[CreateRegion]:
        self.db.execute(
            insert(RegionModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update administative region function
    def update(self, data: RegionModel) -> RegionModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete administative region function
    def delete(self, region: RegionModel) -> None:
        self.db.delete(region)
        self.db.commit()
