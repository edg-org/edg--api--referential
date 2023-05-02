from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.sales.models.SubscriptionTypeModel import SubscriptionTypeModel
from api.sales.schemas.SubscriptionTypeSchema import CreateSubscriptionType

class SubscriptionTypeRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        return self.db.query(func.max(SubscriptionTypeModel.code)).one()[0]
    
    # get all subscription types function
    def list(self, skip: int = 0, limit: int = 100) -> List[SubscriptionTypeModel]:
        return self.db.query(SubscriptionTypeModel).offset(skip).limit(limit).all()

    # get subscription type by id function
    def get(self, id: int) -> SubscriptionTypeModel:
        return self.db.query(SubscriptionTypeModel).where(SubscriptionTypeModel.id == id).first()
    
    # get subscription type code function
    def getbycode(self, code: str) -> SubscriptionTypeModel:
        return self.db.query(SubscriptionTypeModel).where(SubscriptionTypeModel.code == code).first()
    
    # get subscription type name function
    def getbyname(self, name: str) -> SubscriptionTypeModel:
        return self.db.query(SubscriptionTypeModel).where(func.lower(SubscriptionTypeModel.name) == name.lower()).first()
    
    # create subscription type function
    def create(self, data: List[CreateSubscriptionType]) -> List[CreateSubscriptionType]:
        self.db.execute(insert(SubscriptionTypeModel), encoders.jsonable_encoder(data))
        self.db.commit()
        return data

    # update subscription type function
    def update(self, data: SubscriptionTypeModel) -> SubscriptionTypeModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete subscription type function
    def delete(self, subscription: SubscriptionTypeModel) -> None:
        self.db.delete(subscription)
        self.db.commit()