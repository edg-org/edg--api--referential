from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from sqlalchemy import insert, func, and_
from api.electrical.models.EnergySupplyLineModel import EnergySupplyLineModel
from api.electrical.schemas.EnergySupplyLineSchema import CreateEnergySupplyLine

class EnergySupplyLineRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        codemax = self.db.query(
            func.max(EnergySupplyLineModel.code)
        ).one()[0]
        return 0 if codemax is None else codemax

    # get max code of energy supply line by departure city and line type
    def maxcodebycitylinetype(self, city_code: int, line_type_id: int) -> int:
        codemax = (
            self.db.query(func.max(EnergySupplyLineModel.code))
            .where(
                and_(
                    EnergySupplyLineModel.line_type_id == line_type_id,
                    EnergySupplyLineModel.infos["departure_city_code"] == city_code
                )
            ).one()[0]
        )
        return 0 if codemax is None else codemax

    # count total rows of energy supply line by name
    def countbyname(self, name: str) -> int:
        return self.db.query(EnergySupplyLineModel).where(
            func.lower(func.json_unquote(EnergySupplyLineModel.infos["name"])) == name.lower()
        ).count()
    
    # count total rows of energy supply line by code
    def countbycode(self, code: int) -> int:
        return self.db.query(EnergySupplyLineModel).where(
            EnergySupplyLineModel.code == code
        ).count()

    # get all energy supplies function
    def list(self, skip: int = 0, limit: int = 100) -> List[EnergySupplyLineModel]:
        return (
            self.db.query(EnergySupplyLineModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get energy supply line by id function
    def get(self, id: int) -> EnergySupplyLineModel:
        return (
            self.db.query(EnergySupplyLineModel)
            .where(EnergySupplyLineModel.id == id)
            .first()
        )

    # get energy supply line code function
    def getbycode(self, code: int) -> EnergySupplyLineModel:
        return (
            self.db.query(EnergySupplyLineModel)
            .where(EnergySupplyLineModel.code == code)
            .first()
        )

    # get energy supply line name function
    def getbyname(self, name: str) -> EnergySupplyLineModel:
        return (
            self.db.query(EnergySupplyLineModel)
            .where(
                func.lower(
                    EnergySupplyLineModel.infos["name"]
                ) == name.lower()
            )
            .first()
        )

    # check energy supply line name in the city function
    def checklinename(self, departure_city_code: int, name: str) -> int:
        return (
            self.db.query(func.count(EnergySupplyLineModel.id))
            .where(
                and_(
                    EnergySupplyLineModel.infos["departure_city_code"] == departure_city_code,
                    func.lower(func.json_unquote(EnergySupplyLineModel.infos["name"])) == name.lower()
                )
            ).one()[0]
        )

    # create energy supply line function
    def create(self, data: List[CreateEnergySupplyLine]) -> List[CreateEnergySupplyLine]:
        self.db.execute(
            insert(EnergySupplyLineModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update energy supply line function
    def update(self, data: CreateEnergySupplyLine) -> EnergySupplyLineModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete energy supply line function
    def delete(self, meter: EnergySupplyLineModel) -> None:
        self.db.delete(meter)
        self.db.commit()