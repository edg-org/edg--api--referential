from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from sqlalchemy import insert, update, func
from api.salesfinancial.models.SubscriptionTypeModel import SubscriptionTypeModel
from api.salesfinancial.schemas.SubscriptionTypeSchema import CreateSubscriptionType

class SubscriptionTypeRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        codemax = self.db.query(func.max(SubscriptionTypeModel.code)).one()[0]
        return 0 if codemax is None else codemax

    # get all subscription types function
    def list(self, start: int = 0, size: int = 100) -> (int, List[SubscriptionTypeModel]):
        query = self.db.query(SubscriptionTypeModel)
        return query.count(), query.offset(start).limit(size).all()

    # get subscription type by id function
    def get(self, id: int) -> SubscriptionTypeModel:
        return (
            self.db.query(SubscriptionTypeModel)
            .where(SubscriptionTypeModel.id == id)
            .first()
        )

    # get subscription type code function
    def getbycode(self, code: str) -> SubscriptionTypeModel:
        return (
            self.db.query(SubscriptionTypeModel)
            .where(SubscriptionTypeModel.code == code)
            .first()
        )

    # get subscription type name function
    def getbyname(self, name: str) -> SubscriptionTypeModel:
        return (
            self.db.query(SubscriptionTypeModel)
            .where(
                func.lower(SubscriptionTypeModel.name)
                == name.lower()
            )
            .first()
        )

    # create subscription type function
    def create(self, data: List[CreateSubscriptionType]) -> List[CreateSubscriptionType]:
        self.db.execute(
            insert(SubscriptionTypeModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update subscription type function
    def update(self, code: int, data: dict) -> SubscriptionTypeModel:
        self.db.execute(
            update(SubscriptionTypeModel)
            .where(SubscriptionTypeModel.code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=code)

    # delete subscription type function
    def delete(self, subscription: SubscriptionTypeModel) -> None:
        self.db.delete(subscription)
        self.db.commit()
