from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from sqlalchemy import insert, update
from api.configs.Database import get_db
from api.electrical.models.ElectricMeterModel import ElectricMeterModel
from api.electrical.schemas.ElectricMeterSchema import CreateElectricMeter

class ElectricMeterRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db
    
    # count total rows of electric metric by number
    def countbynumber(self, number: str) -> int:
        return self.db.query(ElectricMeterModel).where(
            ElectricMeterModel.meter_number == number
        ).count()
        
    # get all electric meters function
    def list(self, start: int = 0, size: int = 100) -> (int, List[ElectricMeterModel]):
        query = self.db.query(ElectricMeterModel)
        return query.count(), query.offset(start).limit(size).all()

    # get electric meter by id function
    def get(self, id: int) -> ElectricMeterModel:
        return (
            self.db.query(ElectricMeterModel)
            .where(ElectricMeterModel.id == id)
            .first()
        )

    # get electric meter number function
    def getbynumber(self, number: str) -> ElectricMeterModel:
        return (
            self.db.query(ElectricMeterModel)
            .where(ElectricMeterModel.meter_number == number)
            .first()
        )

    # create electric meter function
    def create(self, data: List[CreateElectricMeter]) -> List[CreateElectricMeter]:
        self.db.execute(
            insert(ElectricMeterModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update electric meter function
    def update(self, code: int, data: dict) -> ElectricMeterModel:
        self.db.execute(
            update(ElectricMeterModel)
            .where(ElectricMeterModel.code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=code)

    # delete electric meter function
    def delete(self, meter: ElectricMeterModel) -> None:
        self.db.delete(meter)
        self.db.commit()