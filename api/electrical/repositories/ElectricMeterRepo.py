from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from sqlalchemy import insert, update, select
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
    def list(self, skip: int = 0, limit: int = 100) -> List[ElectricMeterModel]:
        return (
            self.db.query(ElectricMeterModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

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

    def getbycode(self, number: str) -> ElectricMeterModel:
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
    def update(self, number: str, data: dict) -> ElectricMeterModel:
        self.db.execute(
            update(ElectricMeterModel)
            .where(ElectricMeterModel.meter_number == number)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(number=number)

    # delete electric meter function
    def delete(self, meter: ElectricMeterModel) -> None:
        self.db.delete(meter)
        self.db.commit()
    def verif_duplicate(self, name: str, req: str = "True") -> [ElectricMeterModel]:
        stmt = (
            select(ElectricMeterModel)
            .filter(ElectricMeterModel.name.ilike(name))
            .filter(eval(req))
        )
        return self.db.scalars(stmt).all()