from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.electrical.models.MeterDeliveryPointModel import MeterDeliveryPointModel
from api.electrical.schemas.MeterDeliveryPointSchema import CreateMeterDeliveryPoint

class MeterDeliveryPointRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get all meter meter delivery points function
    def list(self, start: int = 0, size: int = 100) -> (int ,List[MeterDeliveryPointModel]):
        query = self.db.query(MeterDeliveryPointModel)
        return query.count(), query.offset(start).limit(size).all()

    # get meter delivery point by id function
    def get(self, id: int) -> MeterDeliveryPointModel:
        return (
            self.db.query(MeterDeliveryPointModel)
            .where(MeterDeliveryPointModel.id == id)
            .first()
        )

    # get by meter number function
    def getbymeternumber(self, number: int) -> MeterDeliveryPointModel:
        return (
            self.db.query(MeterDeliveryPointModel)
            .where(
                MeterDeliveryPointModel.meter_number
                == number
            )
            .first()
        )

    # get by delivery point number function
    def getbydeliverypointnumber(self, number: int) -> MeterDeliveryPointModel:
        return (
            self.db.query(MeterDeliveryPointModel)
            .where(
                MeterDeliveryPointModel.delivery_point_number
                == number
            )
            .first()
        )

    # create meter delivery point function
    def create(self, data: List[CreateMeterDeliveryPoint]) -> List[CreateMeterDeliveryPoint]:
        self.db.execute(
            insert(MeterDeliveryPointModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # delete meter delivery point function
    def delete(self, meter: MeterDeliveryPointModel) -> None:
        self.db.delete(meter)
        self.db.commit()
