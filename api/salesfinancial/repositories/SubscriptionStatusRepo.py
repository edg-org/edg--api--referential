from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from sqlalchemy import insert, update, func
from api.salesfinancial.models.SubscriptionStatusModel import SubscriptionStatusModel
from api.salesfinancial.schemas.SubscriptionStatusSchema import CreateSubscriptionStatus

class SubscriptionStatusRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        codemax = self.db.query(func.max(SubscriptionStatusModel.code)).one()[0]
        return 0 if codemax is None else codemax

    # get all subscription status function
    def list(self, start: int = 0, size: int = 100) -> List[SubscriptionStatusModel]:
        query = self.db.query(SubscriptionStatusModel)
        return query.offset(start).limit(size).all()

    # get subscription status by id function
    def get(self, id: int) -> SubscriptionStatusModel:
        return (
            self.db.query(SubscriptionStatusModel)
            .where(SubscriptionStatusModel.id == id)
            .first()
        )

    # get subscription status code function
    def getbycode(
        self, code: str
    ) -> SubscriptionStatusModel:
        return (
            self.db.query(SubscriptionStatusModel)
            .where(SubscriptionStatusModel.code == code)
            .first()
        )

    # get subscription status name function
    def getbyname(self, name: str) -> SubscriptionStatusModel:
        return (
            self.db.query(SubscriptionStatusModel)
            .where(func.lower(SubscriptionStatusModel.name) == name.lower())
            .first()
        )

    # create subscription status function
    def create(self, data: List[CreateSubscriptionStatus]) -> List[CreateSubscriptionStatus]:
        self.db.execute(
            insert(SubscriptionStatusModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update subscription status function
    def update(self, code: int, data: dict) -> SubscriptionStatusModel:
        self.db.execute(
            update(SubscriptionStatusModel)
            .where(SubscriptionStatusModel.code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=code)

    # delete subscription status function
    def delete(self, subscription: SubscriptionStatusModel) -> None:
        self.db.delete(subscription)
        self.db.commit()
