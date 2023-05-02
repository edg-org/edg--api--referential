from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.geographical.models.CityLevelModel import CityLevelModel
from api.geographical.schemas.CityLevelSchema import CreateCityLevel

#
class CityLevelRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        return self.db.query(func.max(CityLevelModel.code)).one()[0]
    
    # get all city levels function
    def list(self, skip: int = 0, limit: int = 100) -> List[CityLevelModel]:
        return self.db.query(CityLevelModel).offset(skip).limit(limit).all()

    # get city level by id function
    def get(self, id: int) -> CityLevelModel:
        return self.db.query(CityLevelModel).where(CityLevelModel.id == id).first()
    
    # get city level code function
    def getbycode(self, code: str) -> CityLevelModel:
        return self.db.query(CityLevelModel).where(CityLevelModel.code == code).first()
    
    # get city level name function
    def getbyname(self, name: str) -> CityLevelModel:
        return self.db.query(CityLevelModel).where(func.lower(CityLevelModel.name) == name.lower()).first()
    
    # create city level function
    def create(self, data: List[CreateCityLevel]) -> List[CreateCityLevel]:
        self.db.execute(insert(CityLevelModel), encoders.jsonable_encoder(data))
        self.db.commit()
        return data

    # update city level function
    def update(self, data: CityLevelModel) -> CityLevelModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete city level function
    def delete(self, city: CityLevelModel) -> None:
        self.db.delete(city)
        self.db.commit()