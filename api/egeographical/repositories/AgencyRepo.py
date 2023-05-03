from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.egeographical.models.AgencyModel import AgencyModel
from api.egeographical.schemas.AgencySchema import (
    CreateAgency,
)


class AgencyRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max id of agency by area
    def maxcodebyzone(self, area_code: int) -> int:
        return (
            self.db.query(func.max(AgencyModel.code))
            .where(
                AgencyModel.infos["area_code"] == area_code
            )
            .one()[0]
        )

    # get agency id by code function
    def getid_bycode(self, code: int) -> AgencyModel:
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
                func.lower(AgencyModel.infos["name"])
                == name.lower()
            )
            .first()
        )

    # create agency function
    def create(
        self, data: List[CreateAgency]
    ) -> List[CreateAgency]:
        self.db.execute(
            insert(AgencyModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update agency function
    def update(self, data: AgencyModel) -> AgencyModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete agency function
    def delete(self, agency: AgencyModel) -> None:
        self.db.delete(agency)
        self.db.commit()
