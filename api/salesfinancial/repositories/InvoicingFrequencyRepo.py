from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.salesfinancial.models.InvoicingFrequencyModel import InvoicingFrequencyModel
from api.salesfinancial.schemas.InvoicingFrequencySchema import CreateInvoicingFrequency
from sqlalchemy import insert, func, update, select

class InvoicingFrequencyRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        codemax = self.db.query(
            func.max(InvoicingFrequencyModel.code)
        ).one()[0]
        return 0 if codemax is None else codemax

    # get all invoicing frequencies function
    def list(self, skip: int = 0, limit: int = 100) -> List[InvoicingFrequencyModel]:
        return (
            self.db.query(InvoicingFrequencyModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get invoicing frequency by id function
    def get(self, id: int) -> InvoicingFrequencyModel:
        return (
            self.db.query(InvoicingFrequencyModel)
            .where(InvoicingFrequencyModel.id == id)
            .first()
        )

    # get invoicing frequency code function
    def getbycode(
        self, code: int
    ) -> InvoicingFrequencyModel:
        return (
            self.db.query(InvoicingFrequencyModel)
            .where(InvoicingFrequencyModel.code == code)
            .first()
        )

    # get invoicing frequency name function
    def getbyname(self, name: str) -> InvoicingFrequencyModel:
        return (
            self.db.query(InvoicingFrequencyModel)
            .where(
                func.lower(InvoicingFrequencyModel.name)
                == name.lower()
            )
            .first()
        )

     # get invoicing frequency shortname function
    def getbyshortname(self, shortname: str) -> InvoicingFrequencyModel:
        return (
            self.db.query(InvoicingFrequencyModel)
            .where(
                func.lower(InvoicingFrequencyModel.shortname)
                == shortname.lower()
            )
            .first()
        )
    
    # create invoicing frequency function
    def create(self, data: List[CreateInvoicingFrequency]) -> List[CreateInvoicingFrequency]:
        self.db.execute(
            insert(InvoicingFrequencyModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    def update(self, code: int, data: CreateInvoicingFrequency) -> InvoicingFrequencyModel:
        self.db.execute(
            update(InvoicingFrequencyModel)
            .where(InvoicingFrequencyModel.code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=data['code'])

    # delete invoicing frequency function
    def delete(
        self, invoicing: InvoicingFrequencyModel
    ) -> None:
        self.db.delete(invoicing)
        self.db.commit()

    def verif_duplicate(self, name: str, req: str = "True") -> [InvoicingFrequencyModel]:
        stmt = (
            select(InvoicingFrequencyModel)
            .filter(InvoicingFrequencyModel.name.ilike(name))
            .filter(eval(req))
        )
        return self.db.scalars(stmt).all()
