from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.geographical.models.AreaTypeModel import AreaTypeModel
from api.geographical.schemas.AreaTypeSchema import CreateAreaType

class AreaTypeRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        return self.db.query(func.max(AreaTypeModel.code)).one()[0]
    
    # get all area types function
    def list(self, skip: int = 0, limit: int = 100) -> List[AreaTypeModel]:
        return self.db.query(AreaTypeModel).offset(skip).limit(limit).all()

    # get area type by id function
    def get(self, id: int) -> AreaTypeModel:
        return self.db.query(AreaTypeModel).where(AreaTypeModel.id == id).first()
    
    # get area type code function
    def getbycode(self, code: str) -> AreaTypeModel:
        return self.db.query(AreaTypeModel).where(AreaTypeModel.code == code).first()
    
    # get area type name function
    def getbyname(self, name: str) -> AreaTypeModel:
        return self.db.query(AreaTypeModel).where(func.lower(AreaTypeModel.name) == name.lower()).first()
    
    # create area type function
    def create(self, data: List[CreateAreaType]) -> List[CreateAreaType]:
        self.db.execute(insert(AreaTypeModel), encoders.jsonable_encoder(data))
        self.db.commit()
        return data

    # update area type function
    def update(self, data: AreaTypeModel) -> AreaTypeModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete area type function
    def delete(self, area: AreaTypeModel) -> None:
        self.db.delete(area)
        self.db.commit()