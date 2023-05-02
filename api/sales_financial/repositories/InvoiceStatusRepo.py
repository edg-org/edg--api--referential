from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.sales_financial.models.InvoiceStatusModel import InvoiceStatusModel
from api.sales_financial.schemas.InvoiceStatusSchema import CreateInvoiceStatus

class InvoiceStatusRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        return self.db.query(func.max(InvoiceStatusModel.code)).one()[0]
    
    # get all subscription status function
    def list(self, skip: int = 0, limit: int = 100) -> List[InvoiceStatusModel]:
        return self.db.query(InvoiceStatusModel).offset(skip).limit(limit).all()

    # get subscription status by id function
    def get(self, id: int) -> InvoiceStatusModel:
        return self.db.query(InvoiceStatusModel).where(InvoiceStatusModel.id == id).first()
    
    # get subscription status code function
    def getbycode(self, code: str) -> InvoiceStatusModel:
        return self.db.query(InvoiceStatusModel).where(InvoiceStatusModel.code == code).first()
    
    # get subscription status name function
    def getbyname(self, name: str) -> InvoiceStatusModel:
        return self.db.query(InvoiceStatusModel).where(func.lower(InvoiceStatusModel.name) == name.lower()).first()
    
    # create subscription status function
    def create(self, data: List[CreateInvoiceStatus]) -> List[CreateInvoiceStatus]:
        self.db.execute(insert(InvoiceStatusModel), encoders.jsonable_encoder(data))
        self.db.commit()
        return data

    # update subscription status function
    def update(self, data: InvoiceStatusModel) -> InvoiceStatusModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete subscription status function
    def delete(self, subscription: InvoiceStatusModel) -> None:
        self.db.delete(subscription)
        self.db.commit()