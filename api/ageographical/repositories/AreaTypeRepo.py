from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from sqlalchemy import select, insert, update, func
from api.ageographical.models.AreaTypeModel import AreaTypeModel
from api.ageographical.schemas.AreaTypeSchema import CreateAreaType, AreaTypeUpdate

#
class AreaTypeRepo:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        codemax = self.db.query(
            func.max(AreaTypeModel.code)
        ).one()[0]
        return 0 if codemax is None else codemax

    # get all area types function
    def list(self, skip: int = 0, limit: int = 100) -> List[AreaTypeModel]:
        return (
            self.db.query(AreaTypeModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get area type by id function
    def get(self, id: int) -> AreaTypeModel:
        return (
            self.db.query(AreaTypeModel)
            .where(AreaTypeModel.id == id)
            .first()
        )

    # get area type no hierarchical function
    def no_hierarchical_type(self) -> AreaTypeModel:
        return (
            self.db.execute(
                select(func.lower(AreaTypeModel.name))
                .where(AreaTypeModel.is_hierarchical == False)
            )
            .scalars()
            .all()
        )
        
    # get area type code function
    def getbycode(self, code: str) -> AreaTypeModel:
        return (
            self.db.query(AreaTypeModel)
            .where(AreaTypeModel.code == code)
            .first()
        )

    # get area type name function
    def getbyname(self, name: str) -> AreaTypeModel:
        return (
            self.db.query(AreaTypeModel)
            .where(func.lower(AreaTypeModel.name) == name.lower())
            .first()
        )

    # create area type function
    def create(self, data: List[CreateAreaType]) -> List[CreateAreaType]:
        self.db.execute(
            insert(AreaTypeModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update area type function
    def update(self, code: int, data: AreaTypeUpdate) -> AreaTypeModel:
        self.db.execute(
            update(AreaTypeModel)
            .where(AreaTypeModel.code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=code)

    # delete area type function
    def delete(self, area: AreaTypeModel) -> None:
        self.db.delete(area)
        self.db.commit()