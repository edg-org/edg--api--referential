from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.salesfinancial.models.PricingHistoryModel import PricingHistoryModel
from api.salesfinancial.schemas.PricingHistorySchema import CreatePricingHistory

class PricingHistoryRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        codemax = self.db.query(func.max(PricingHistoryModel.code)).one()[0]
        return 0 if codemax is None else codemax

    # get all pricing histories function
    def list(self, start: int = 0, size: int = 100) -> List[PricingHistoryModel]:
        query = self.db.query(PricingHistoryModel)
        return query.offset(start).limit(size).all()

    # get pricing history by id function
    def get(self, id: int) -> PricingHistoryModel:
        return (
            self.db.query(PricingHistoryModel)
            .where(PricingHistoryModel.id == id)
            .first()
        )

    # get pricing history code function
    def getbycode(self, code: str) -> PricingHistoryModel:
        return (
            self.db.query(PricingHistoryModel)
            .where(PricingHistoryModel.code == code)
            .first()
        )

    # get pricing history name function
    def getbyname(self, name: str) -> PricingHistoryModel:
        return (
            self.db.query(PricingHistoryModel)
            .where(func.lower(PricingHistoryModel.name) == name.lower())
            .first()
        )

    # create pricing history function
    def create(self, data: List[CreatePricingHistory]) -> List[CreatePricingHistory]:
        self.db.execute(
            insert(PricingHistoryModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data
