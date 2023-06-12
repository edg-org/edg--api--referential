from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from sqlalchemy import insert, func, update
from api.ageographical.models.DeliveryPointModel import DeliveryPointModel
from api.ageographical.schemas.DeliveryPointSchema import CreateDeliveryPoint, DeliveryPointSchema

class DeliveryPointRepo:
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        codemax = (
            self.db.query(func.max(DeliveryPointModel.code))
            .one()[0]
        )
        return 0 if codemax is None else codemax

    # get all delivery points function
    def list(self, start: int = 0, size: int = 100) -> (int, List[DeliveryPointModel]):
        query = self.db.query(DeliveryPointModel)
        return query.count(), query.offset(start).limit(size).all()

    # get delivery point by id function
    def get(self, id: int) -> DeliveryPointModel:
        return (
            self.db.query(DeliveryPointModel)
            .where(DeliveryPointModel.id == id)
            .first()
        )

     # count total rows of delivery point by number
    def countbynumber(self, number: int) -> int:
        return (
            self.db.query(DeliveryPointModel)
            .where(DeliveryPointModel.delivery_point_number == number)
            .count()
        )

    # get delivery point number function
    def getbynumber(self, number: int) -> DeliveryPointModel:
        return (
            self.db.query(DeliveryPointModel)
            .where(DeliveryPointModel.delivery_point_number == number)
            .first()
        )

    # get max number of delivery point by area
    def maxnumberyarea(self, area_code: int) -> int:
        numbermax = (
            self.db.query(func.max(DeliveryPointModel.delivery_point_number))
            .where(DeliveryPointModel.infos["area_code"] == area_code)
            .one()[0]
        )
        return 0 if numbermax is None else numbermax

    # create delivery point function
    def create(self, data: List[CreateDeliveryPoint]) -> List[CreateDeliveryPoint]:
        self.db.execute(
            insert(DeliveryPointModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update delivery point function
    def update(self, number: int, data: dict) -> DeliveryPointModel:
        self.db.execute(
            update(DeliveryPointModel)
            .where(DeliveryPointModel.delivery_point_number == number)
            .values(**data)
        )
        self.db.commit()
        return self.getbynumber(number=number)

    # delete delivery point function
    def delete(self, meter: DeliveryPointModel) -> None:
        self.db.delete(meter)
        self.db.commit()