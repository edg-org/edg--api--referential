from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from sqlalchemy import insert, func, and_, update
from api.ageographical.models.CityModel import CityModel
from api.ageographical.schemas.CitySchema import CreateCity, CityUpdate, CitySearchParams

#
class CityRepo:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    # get max code of city by prefecture
    def maxcodebypref(self, prefecture_id: int) -> int:
        codemax = (
            self.db.query(func.max(CityModel.code))
            .where(CityModel.prefecture_id == prefecture_id)
            .one()[0]
        )
        return 0 if codemax is None else codemax

    # get max zipcode of city by prefecture
    def maxzipcodebypref(self, prefecture_id: int) -> int:
        codemax = (
            self.db.query(func.max(int(CityModel.zipcode)))
            .where(CityModel.prefecture_id == prefecture_id)
            .one()[0]
        )
        return 0 if codemax is None else codemax
    
    # get max zipcode of city by prefecture and city level
    def maxzipcodebyprefandlevel(self, prefecture_id: int, city_level_id: int) -> int:
        codemax = (
            self.db.query(func.max(int(CityModel.zipcode)))
            .where(
                and_(
                    CityModel.city_level_id == city_level_id,
                    CityModel.prefecture_id == prefecture_id
                )
            )
            .one()[0]
        )
        return 0 if codemax is None else codemax

    # count total rows of city by name
    def countbyname(self, name: str) -> int:
        return self.db.query(CityModel).where(
            func.lower(func.json_unquote(CityModel.infos["name"])) == name.lower()
        ).count()
    
    # count total rows of city by code
    def countbycode(self, code: int) -> int:
        return (
            self.db.query(CityModel)
            .where(CityModel.code == code)
            .count()
        )

    # count total rows of city by zipcode
    def countbyzipcode(self, zipcode: str) -> CityModel:
        return (
            self.db.query(CityModel)
            .where(CityModel.zipcode == zipcode)
            .count()
        )

    # get city code by code function
    def getidbycode(self, code: int) -> CityModel:
        return (
            self.db.query(CityModel.id)
            .where(CityModel.code == code)
            .one()[0]
        )

    # get all cities function
    def list(self, start: int = 0, size: int = 100) -> (int, List[CityModel]):
        query = self.db.query(CityModel)
        return query.count(), query.offset(start).limit(size).all()

    # get city by id function
    def get(self, id: int) -> CityModel:
        return (
            self.db.query(CityModel)
            .where(CityModel.id == id)
            .first()
        )

    # get city code function
    def getbycode(self, code: int) -> CityModel:
        return (
            self.db.query(CityModel)
            .where(CityModel.code == code)
            .first()
        )

    # get city name function
    def getbyname(self, name: str) -> CityModel:
        return (
            self.db.query(CityModel)
            .where(func.lower(func.json_unquote(CityModel.infos["name"])) == name.lower())
            .all()
        )
    
    # check city name in the prefecture function
    def checkcityname(self, prefecture_id: int, name: str) -> int:
        return (
            self.db.query(func.count(CityModel.id))
            .where(
                and_(
                    CityModel.prefecture_id == prefecture_id,
                    func.lower(func.json_unquote(CityModel.infos["name"])) == name.lower()
                )
            ).one()[0]
        )

    # get city by zipcode function
    def getbyzipcode(self, zipcode: str) -> CityModel:
        return (
            self.db.query(CityModel)
            .where(CityModel.zipcode == zipcode)
            .first()
        )

    # get city by parameters function
    def search(self, query_params: CitySearchParams) -> CityModel:
        return (
            self.db.query(CityModel)
            .where(
                and_(
                    CityModel.code == query_params.code
                    if query_params.code is not None else True,
                    CityModel.zipcode == query_params.zipcode
                    if query_params.zipcode is not None else True
                )
            ).first()
        )

    # create city function
    def create(self, data: List[CreateCity]) -> List[CreateCity]:
        self.db.execute(
            insert(CityModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update city function
    def update(self, code: int,  data: dict) -> CityModel:
        self.db.execute(
            update(CityModel)
            .where(CityModel.code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=code)

    # delete city function
    def delete(self, city: CityModel) -> None:
        self.db.delete(city)
        self.db.commit()