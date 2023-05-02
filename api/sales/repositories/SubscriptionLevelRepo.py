from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.sales.models.SubscriptionLevelModel import SubscriptionLevelModel
from api.sales.schemas.SubscriptionLevelSchema import CreateSubscriptionLevel

class SubscriptionLevelRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        return self.db.query(func.max(SubscriptionLevelModel.code)).one()[0]
    
    # get all subscription levels function
    def list(self, skip: int = 0, limit: int = 100) -> List[SubscriptionLevelModel]:
        return self.db.query(SubscriptionLevelModel).offset(skip).limit(limit).all()

    # get subscription level by id function
    def get(self, id: int) -> SubscriptionLevelModel:
        return self.db.query(SubscriptionLevelModel).where(SubscriptionLevelModel.id == id).first()
    
    # get subscription level code function
    def getbycode(self, code: str) -> SubscriptionLevelModel:
        return self.db.query(SubscriptionLevelModel).where(SubscriptionLevelModel.code == code).first()
    
    # get subscription level name function
    def getbyname(self, name: str) -> SubscriptionLevelModel:
        return self.db.query(SubscriptionLevelModel).where(func.lower(SubscriptionLevelModel.name) == name.lower()).first()
    
    # create subscription level function
    def create(self, data: List[CreateSubscriptionLevel]) -> List[CreateSubscriptionLevel]:
        self.db.execute(insert(SubscriptionLevelModel), encoders.jsonable_encoder(data))
        self.db.commit()
        return data

    # update subscription level function
    def update(self, data: SubscriptionLevelModel) -> SubscriptionLevelModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete subscription level function
    def delete(self, subscription: SubscriptionLevelModel) -> None:
        self.db.delete(subscription)
        self.db.commit()