from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.egeographical.models.PrefectureModel import (
    PrefectureModel,
)
from api.egeographical.schemas.PrefectureSchema import (
    CreatePrefecture,
)


class PrefectureRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # count total rows of natural region
    def countrows(self) -> int:
        return self.db.query(PrefectureModel).count()

    # get max code of prefecture by region
    def maxcode_byzone(self, zone_code: int) -> int:
        return (
            self.db.query(func.max(PrefectureModel.code))
            .where(
                PrefectureModel.infos["zone_code"]
                == zone_code
            )
            .one()[0]
        )

    # get prefecture id by code function
    def getidbycode(self, code: int) -> PrefectureModel:
        return (
            self.db.query(PrefectureModel.id)
            .where(PrefectureModel.code == code)
            .one()[0]
        )

    # get all prefectures function
    def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[PrefectureModel]:
        return (
            self.db.query(PrefectureModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get prefecture by id function
    def get(self, id: int) -> PrefectureModel:
        return (
            self.db.query(PrefectureModel)
            .where(PrefectureModel.id == id)
            .first()
        )

    # get prefecture by id function
    def get(self, number: str) -> PrefectureModel:
        return (
            self.db.query(PrefectureModel)
            .where(
                PrefectureModel.prefecture_number == number
            )
            .first()
        )

    # get prefecture code function
    def getbycode(self, code: int) -> PrefectureModel:
        return (
            self.db.query(PrefectureModel)
            .where(PrefectureModel.code == code)
            .first()
        )

    # get prefecture name function
    def getbyname(self, name: str) -> PrefectureModel:
        return (
            self.db.query(PrefectureModel)
            .where(
                func.lower(PrefectureModel.infos["name"])
                == name.lower()
            )
            .first()
        )

    # create prefecture function
    def create(
        self, data: List[CreatePrefecture]
    ) -> List[CreatePrefecture]:
        self.db.execute(
            insert(PrefectureModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update prefecture function
    def update(
        self, data: PrefectureModel
    ) -> PrefectureModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete prefecture function
    def delete(self, prefecture: PrefectureModel) -> None:
        self.db.delete(prefecture)
        self.db.commit()
