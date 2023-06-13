from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func, update
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.ageographical.models.PrefectureModel import PrefectureModel
from api.ageographical.schemas.PrefectureSchema import CreatePrefecture, PrefectureUpdate

#
class PrefectureRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # count total rows of prefecture
    def countrows(self) -> int:
        return self.db.query(PrefectureModel).count()

    # count total rows of prefecture by name
    def countbyname(self, name: str) -> int:
        return (
            self.db.query(PrefectureModel)
            .where(
            func.lower(PrefectureModel.name) == name.lower())
            .count()
        )
    
    # count total rows of prefecture by code
    def countbycode(self, code: int) -> int:
        return (
            self.db.query(PrefectureModel)
            .where(PrefectureModel.code == code)
            .count()
        )

    # get max code of prefecture by region
    def maxcodebyzone(self, zone_code: int) -> int:
        codemax = (
            self.db.query(func.max(PrefectureModel.code))
            .where(PrefectureModel.infos["zone_code"] == zone_code)
            .one()[0]
        )
        return 0 if codemax is None else codemax

    # get prefecture id by code function
    def getidbycode(self, code: int) -> PrefectureModel:
        return (
            self.db.query(PrefectureModel.id)
            .where(PrefectureModel.code == code)
            .one()[0]
        )

    # get prefecture id by name function
    def getidbyname(self, name: str) -> PrefectureModel:
        return (
            self.db.query(PrefectureModel.id)
            .where(func.lower(PrefectureModel.name) == name.lower())
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
            ).first()
        )

    # get prefecture code function
    def getbycode(self, code: int) -> PrefectureModel:
        return (
            self.db.query(PrefectureModel).where(PrefectureModel.code == code).first()
        )

    # get prefecture name function
    def getbyname(self, name: str) -> PrefectureModel:
        return (
            self.db.query(PrefectureModel).where(
                func.lower(func.json_unquote(PrefectureModel.name))== name.lower()
            ).first()
        )

    # create prefecture function
    def create(self, data: List[CreatePrefecture]) -> List[CreatePrefecture]:
        self.db.execute(
            insert(PrefectureModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update prefecture function
    def update(self, code: int, data: dict) -> PrefectureModel:
        self.db.execute(
            update(PrefectureModel)
            .where(PrefectureModel.code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=code)

    # delete prefecture function
    def delete(self, prefecture: PrefectureModel) -> None:
        self.db.delete(prefecture)
        self.db.commit()
