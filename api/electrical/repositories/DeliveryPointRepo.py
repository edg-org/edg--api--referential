from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.electrical.models.DeliveryPointModel import DeliveryPointModel
from api.electrical.schemas.DeliveryPointSchema import CreateDeliveryPoint

class DeliveryPointRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        codemax = self.db.query(
            func.max(DeliveryPointModel.code)
        ).one()[0]
        return 0 if codemax is None else codemax

    # get all delivery points function
    def list(self, skip: int = 0, limit: int = 100) -> List[DeliveryPointModel]:
        return (
            self.db.query(DeliveryPointModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get delivery point by id function
    def get(self, id: int) -> DeliveryPointModel:
        return (
            self.db.query(DeliveryPointModel)
            .where(DeliveryPointModel.id == id)
            .first()
        )

    # get delivery point number function
    def getbynumber(self, number: str) -> DeliveryPointModel:
        return (
            self.db.query(DeliveryPointModel)
            .where(
                func.lower(DeliveryPointModel.delivery_point_number) == number.lower()
            )
            .first()
        )

    # get delivery point name function
    def getbyname(self, name: str) -> DeliveryPointModel:
        return (
            self.db.query(DeliveryPointModel)
            .where(
                func.lower(DeliveryPointModel.infos["name"]) == name.lower()
            )
            .first()
        )

    # create delivery point function
    def create(self, data: List[CreateDeliveryPoint]) -> List[CreateDeliveryPoint]:
        self.db.execute(
            insert(DeliveryPointModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update delivery point function
    def update(self, data: CreateDeliveryPoint) -> DeliveryPointModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete delivery point function
    def delete(self, meter: DeliveryPointModel) -> None:
        self.db.delete(meter)
        self.db.commit()
