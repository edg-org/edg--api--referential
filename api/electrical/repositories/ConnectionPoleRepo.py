from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.electrical.models.ConnectionPoleModel import ConnectionPoleModel
from api.electrical.schemas.ConnectionPoleSchema import CreateConnectionPole


class ConnectionPoleRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        codemax = self.db.query(
            func.max(ConnectionPoleModel.code)
        ).one()[0]
        return 0 if codemax is None else codemax
    
    # get max number of connection area by area
    def maxnumberbyarea(
        self, 
        area_code: int
    ) -> int:
        codemax = (
            self.db.query(func.max(ConnectionPoleModel.connection_pole_number))
            .where(
                ConnectionPoleModel.infos["area_code"] == area_code
            ).one()[0]
        )
        return 0 if codemax is None else codemax

    # get all connection poles function
    def list(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ConnectionPoleModel]:
        return (
            self.db.query(ConnectionPoleModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get connection pole by id function
    def get(self, id: int) -> ConnectionPoleModel:
        return (
            self.db.query(ConnectionPoleModel)
            .where(ConnectionPoleModel.id == id)
            .first()
        )

    # get connection pole number function
    def getbynumber(
        self, 
        number: int
    ) -> ConnectionPoleModel:
        return (
            self.db.query(ConnectionPoleModel)
            .where(ConnectionPoleModel.connection_pole_number == number)
            .first()
        )

    # get connection pole name function
    def getbyname(self, name: str) -> ConnectionPoleModel:
        return (
            self.db.query(ConnectionPoleModel)
            .where(func.lower(ConnectionPoleModel.infos["name"]) == name.lower())
            .first()
        )

     # count total rows of connection pole by number
    def countbynumber(self, number: int) -> ConnectionPoleModel:
        return (
            self.db.query(ConnectionPoleModel)
            .where(ConnectionPoleModel.connection_pole_number == number)
            .count()
        )

    # create connection pole function
    def create(self, data: List[CreateConnectionPole]) -> List[CreateConnectionPole]:
        self.db.execute(
            insert(ConnectionPoleModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update connection pole function
    def update(self, data: CreateConnectionPole) -> ConnectionPoleModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete connection pole function
    def delete(self, meter: ConnectionPoleModel) -> None:
        self.db.delete(meter)
        self.db.commit()