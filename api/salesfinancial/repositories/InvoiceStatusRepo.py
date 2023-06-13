from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.salesfinancial.models.InvoiceStatusModel import InvoiceStatusModel
from api.salesfinancial.schemas.InvoiceStatusSchema import CreateInvoiceStatus
from sqlalchemy import insert, func, update
class InvoiceStatusRepo:
    db: Session

    def __init__(
        self, 
        db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        codemax = self.db.query(
            func.max(InvoiceStatusModel.code)
        ).one()[0]
        return 0 if codemax is None else codemax

    # get all subscription status function
    def list(self, skip: int = 0, limit: int = 100) -> List[InvoiceStatusModel]:
        return (
            self.db.query(InvoiceStatusModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get subscription status by id function
    def get(self, id: int) -> InvoiceStatusModel:
        return (
            self.db.query(InvoiceStatusModel)
            .where(InvoiceStatusModel.id == id)
            .first()
        )

    # get subscription status code function
    def getbycode(self, code: int) -> InvoiceStatusModel:
        return (
            self.db.query(InvoiceStatusModel)
            .where(InvoiceStatusModel.code == code)
            .first()
        )

    # get subscription status name function
    def getbyname(self, name: str) -> InvoiceStatusModel:
        return (
            self.db.query(InvoiceStatusModel)
            .where(
                func.lower(InvoiceStatusModel.name)
                == name.lower()
            )
            .first()
        )

    # create subscription status function
    def create(self, data: List[CreateInvoiceStatus]) -> List[CreateInvoiceStatus]:
        self.db.execute(
            insert(InvoiceStatusModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update subscription status function
    def update(self, code: int, data: CreateInvoiceStatus) -> InvoiceStatusModel:
        self.db.execute(
            update(InvoiceStatusModel)
            .where(InvoiceStatusModel.code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=code)

    # delete subscription status function
    def delete(
        self, subscription: InvoiceStatusModel
    ) -> None:
        self.db.delete(subscription)
        self.db.commit()
