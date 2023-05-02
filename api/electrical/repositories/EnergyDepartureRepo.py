from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.electrical.models.EnergyDepartureModel import (
    EnergyDepartureModel,
)
from api.electrical.schemas.EnergyDepartureSchema import (
    CreateEnergyDeparture,
)


class EnergyDepartureRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        return self.db.query(
            func.max(EnergyDepartureModel.code)
        ).one()[0]

    # get all energy departures function
    def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[EnergyDepartureModel]:
        return (
            self.db.query(EnergyDepartureModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get energy departure by id function
    def get(self, id: int) -> EnergyDepartureModel:
        return (
            self.db.query(EnergyDepartureModel)
            .where(EnergyDepartureModel.id == id)
            .first()
        )

    # get energy departure code function
    def getbycode(self, code: int) -> EnergyDepartureModel:
        return (
            self.db.query(EnergyDepartureModel)
            .where(EnergyDepartureModel.code == code)
            .first()
        )

    # get energy departure name function
    def getbyname(self, name: str) -> EnergyDepartureModel:
        return (
            self.db.query(EnergyDepartureModel)
            .where(
                func.lower(
                    EnergyDepartureModel.infos["name"]
                )
                == name.lower()
            )
            .first()
        )

    # create energy departure function
    def create(
        self, data: List[CreateEnergyDeparture]
    ) -> List[CreateEnergyDeparture]:
        self.db.execute(
            insert(EnergyDepartureModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update energy departure function
    def update(
        self, data: EnergyDepartureModel
    ) -> EnergyDepartureModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete energy departure function
    def delete(self, meter: EnergyDepartureModel) -> None:
        self.db.delete(meter)
        self.db.commit()
