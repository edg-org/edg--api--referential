from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.electrical.models.ConnectionPointModel import (
    ConnectionPointModel,
)
from api.electrical.schemas.ConnectionPointSchema import (
    CreateConnectionPoint,
)


class ConnectionPointRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        return self.db.query(
            func.max(ConnectionPointModel.code)
        ).one()[0]

    # get all connection points function
    def list(
        self, skip: int = 0, limit: int = 100
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
        self, number: int
    ) -> ConnectionPointModel:
        return (
            self.db.query(ConnectionPointModel)
            .where(
                ConnectionPointModel.connection_point_number
                == number
            )
            .first()
        )

    # get connection point name function
    def getbyname(self, name: str) -> ConnectionPointModel:
        return (
            self.db.query(ConnectionPointModel)
            .where(
                func.lower(
                    ConnectionPointModel.infos["name"]
                )
                == name.lower()
            )
            .first()
        )

    # create connection point function
    def create(
        self, data: List[CreateConnectionPoint]
    ) -> List[CreateConnectionPoint]:
        self.db.execute(
            insert(ConnectionPointModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update connection point function
    def update(
        self, data: ConnectionPointModel
    ) -> ConnectionPointModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete connection point function
    def delete(self, meter: ConnectionPointModel) -> None:
        self.db.delete(meter)
        self.db.commit()
