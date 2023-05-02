from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.electrical.models.PowerModeModel import (
    PowerModeModel,
)
from api.electrical.schemas.PowerModeSchema import (
    CreatePowerMode,
)


class PowerModeRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        return self.db.query(
            func.max(PowerModeModel.code)
        ).one()[0]

    # get all power modes function
    def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[PowerModeModel]:
        return (
            self.db.query(PowerModeModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get power mode by id function
    def get(self, id: int) -> PowerModeModel:
        return (
            self.db.query(PowerModeModel)
            .where(PowerModeModel.id == id)
            .first()
        )

    # get power mode code function
    def getbycode(self, code: str) -> PowerModeModel:
        return (
            self.db.query(PowerModeModel)
            .where(PowerModeModel.code == code)
            .first()
        )

    # get power mode name function
    def getbyname(self, name: str) -> PowerModeModel:
        return (
            self.db.query(PowerModeModel)
            .where(
                func.lower(PowerModeModel.name)
                == name.lower()
            )
            .first()
        )

    # create power mode function
    def create(
        self, data: List[CreatePowerMode]
    ) -> List[CreatePowerMode]:
        self.db.execute(
            insert(PowerModeModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update power mode function
    def update(
        self, data: PowerModeModel
    ) -> PowerModeModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete power mode function
    def delete(self, meter: PowerModeModel) -> None:
        self.db.delete(meter)
        self.db.commit()
