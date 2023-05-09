from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.ageographical.models.AgencyModel import AgencyModel
from api.ageographical.schemas.AgencySchema import CreateAgency, AgencyUpdate

#
class AgencyRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max id of agency by city
    def maxcodebycity(self, city_code: int) -> int:
        codemax = (
            self.db.query(func.max(AgencyModel.code))
            .where(
                AgencyModel.infos["city_code"] == city_code
            ).one()[0]
        )
        return 0 if codemax is None else codemax

    # count total rows of agency by name
    def countbyname(self, name: str) -> int:
        return self.db.query(AgencyModel).where(
            func.lower(
                func.json_unquote(AgencyModel.infos["name"])
            ) == name.lower()
        ).count()
    
    # count total rows of agency by code
    def countbycode(self, code: int) -> int:
        return self.db.query(AgencyModel).where(
            AgencyModel.code == code
        ).count()

    # get agency id by code function
    def getidbycode(self, code: int) -> AgencyModel:
        return (
            self.db.query(AgencyModel.id)
            .where(AgencyModel.code == code)
            .one()[0]
        )

    # get all agencys function
    def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[AgencyModel]:
        return (
            self.db.query(AgencyModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get agency by id function
    def get(self, id: int) -> AgencyModel:
        return (
            self.db.query(AgencyModel)
            .where(AgencyModel.id == id)
            .first()
        )

    # get agency code function
    def getbycode(self, code: str) -> AgencyModel:
        return (
            self.db.query(AgencyModel)
            .where(AgencyModel.code == code)
            .first()
        )

    # get agency name function
    def getbyname(self, name: str) -> AgencyModel:
        return (
            self.db.query(AgencyModel)
            .where(
                func.lower(
                    func.json_unquote(AgencyModel.infos["name"])
                ) == name.lower()
            ).first()
        )

    # create agency function
    def create(self, data: List[CreateAgency]) -> List[CreateAgency]:
        self.db.execute(
            insert(AgencyModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update agency function
    def update(self, data: CreateAgency) -> AgencyModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete agency function
    def delete(self, agency: AgencyModel) -> None:
        self.db.delete(agency)
        self.db.commit()