from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.electrical.models.ConnectionPointModel import ConnectionPointModel
from api.electrical.schemas.ConnectionPointSchema import CreateConnectionPoint


class ConnectionPointRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        codemax = self.db.query(
            func.max(ConnectionPointModel.code)
        ).one()[0]
        return 0 if codemax is None else codemax
    
    # get max number of connection area by area
    def maxnumberbyarea(
        self, 
        area_code: int
    ) -> int:
        codemax = (
            self.db.query(func.max(ConnectionPointModel.connection_point_number))
            .where(
                ConnectionPointModel.infos["area_code"] == area_code
            ).one()[0]
        )
        return 0 if codemax is None else codemax

    # get all connection points function
    def list(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ConnectionPointModel]:
        return (
            self.db.query(ConnectionPointModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get connection point by id function
    def get(self, id: int) -> ConnectionPointModel:
        return (
            self.db.query(ConnectionPointModel)
            .where(ConnectionPointModel.id == id)
            .first()
        )

    # get connection point number function
    def getbynumber(
        self, number: str
    ) -> ConnectionPointModel:
        return (
            self.db.query(ConnectionPointModel)
            .where(
                ConnectionPointModel.connection_point_number == number
            ).first()
        )

    # get connection point name function
    def getbyname(self, name: str) -> ConnectionPointModel:
        return (
            self.db.query(ConnectionPointModel)
            .where(
                func.lower(ConnectionPointModel.infos["name"]) == name.lower()
            ).first()
        )

     # count total rows of connection point by number
    def countbynumber(self, number: str) -> ConnectionPointModel:
        return (
            self.db.query(ConnectionPointModel).where(
                ConnectionPointModel.connection_point_number == number
            ).count()
        )

    # create connection point function
    def create(self, data: List[CreateConnectionPoint]) -> List[CreateConnectionPoint]:
        self.db.execute(
            insert(ConnectionPointModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update connection point function
    def update(self, data: CreateConnectionPoint) -> ConnectionPointModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete connection point function
    def delete(self, meter: ConnectionPointModel) -> None:
        self.db.delete(meter)
        self.db.commit()
