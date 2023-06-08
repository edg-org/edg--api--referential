from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from sqlalchemy import insert, update, func, and_, or_
from api.ageographical.models.AreaModel import AreaModel
from api.ageographical.schemas.AreaSchema import CreateArea

#
class AreaRepo:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    # get max code of area by city and area type
    def maxcodebycityandtype(self, city_code: int, area_type_id: int) -> int:
        codemax = (
            self.db.query(func.max(AreaModel.code))
            .where(
                and_(
                    AreaModel.area_type_id == area_type_id,
                    AreaModel.infos["city_code"] == city_code
                )
            )
            .one()[0]
        )
        return 0 if codemax is None else codemax
    
    # get max zipcode of area by city
    def maxzipcodebycity(self, city_id: int) -> int:
        codemax = (
            self.db.query(func.max(int(AreaModel.zipcode)))
            .where(AreaModel.city_id == city_id)
            .one()[0]
        )
        return 0 if codemax is None else codemax
    
    # get max code of area by hierarchical area and type
    def maxcodebyareaandtype(self, hierarchical_area_code: int, area_type_id: int) -> int:
        codemax = (
            self.db.query(func.max(AreaModel.code))
            .where(AreaModel.infos["hierarchical_area_code"] == hierarchical_area_code)
            .one()[0]
        )
        return 0 if codemax is None else codemax

    # count total rows of area by name
    def countbyname(self, name: str) -> int:
        return self.db.query(AreaModel).where(
            func.lower(func.json_unquote(AreaModel.infos["name"])) == name.lower()
        ).count()
    
    # check area name by city function
    def checkname_by_citycode(self, city_code: int, name: str) -> int:
        return (
            self.db.query(func.count(AreaModel.id))
            .where(
                and_(
                    AreaModel.infos["city_code"] == city_code,
                    func.lower(func.json_unquote(AreaModel.infos["name"])) == name.lower()
                )
            ).one()[0]
        )
    
    # check area name by hierarchical area function
    def checkname_by_hierarchy(self, hierarchical_area_code: int, name: str) -> int:
        return (
            self.db.query(func.count(AreaModel.id))
            .where(
                and_(
                    AreaModel.infos["hierarchical_area_code"] == hierarchical_area_code,
                    func.lower(func.json_unquote(AreaModel.infos["name"])) == name.lower()
                )
            ).one()[0]
        )
    
    # count total rows of area by code
    def countbycode(self, code: int) -> int:
        return (
            self.db.query(AreaModel)
            .where(AreaModel.code == code)
            .count()
        )

    # get area id by code function
    def getidbycode(self, code: int) -> AreaModel:
        return (
            self.db.query(AreaModel.id)
            .where(AreaModel.code == code)
            .one()[0]
        )
    
    # check area name in the place function
    def checkareaname(self, place_code: int, name: str) -> int:
        return (
            self.db.query(func.count(AreaModel.id))
            .where(
                and_(
                    or_(
                        AreaModel.infos["city_code"] == place_code,
                        AreaModel.infos["hierarchical_area_code"] == place_code,
                    ),
                    func.lower(func.json_unquote(AreaModel.infos["name"])) == name.lower()
                )
            ).one()[0]
        )

    # get all areas function
    def list(
        self, 
        skip: int = 0, 
        limit: int = 100
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
            .where(
                AreaModel.id == id
            ).first()
        )

    # get area id by code function
    def getidbycode(self, code: int) -> AreaModel:
        return (
            self.db.query(AreaModel.id)
            .where(
                AreaModel.code == code
            ).one()[0]
        )

    # get area code function
    def getbycode(self, code: int) -> AreaModel:
        return (
            self.db.query(AreaModel)
            .where(AreaModel.code == code)
            .first()
        )

    # get area name function
    def getbyname(self, name: str) -> AreaModel:
        return (
            self.db.query(AreaModel)
            .where(func.lower(func.json_unquote(AreaModel.infos["name"])) == name.lower())
            .first()
        )

    # create area function
    def create(self, data: List[CreateArea]) -> List[CreateArea]:
        self.db.execute(
            insert(AreaModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update area function
    def update(self, code: int, data: dict) -> AreaModel:
        self.db.execute(
            update(AreaModel)
            .where(AreaModel.code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=code)

    # delete area function
    def delete(self, area: AreaModel) -> None:
        self.db.delete(area)
        self.db.commit()