from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.sales.models.ContactTypeModel import ContactTypeModel
from api.sales.schemas.ContactTypeSchema import CreateContactType

class ContactTypeRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        return self.db.query(func.max(ContactTypeModel.code)).one()[0]
    
    # get all contact types function
    def list(self, skip: int = 0, limit: int = 100) -> List[ContactTypeModel]:
        return self.db.query(ContactTypeModel).offset(skip).limit(limit).all()

    # get contact type by id function
    def get(self, id: int) -> ContactTypeModel:
        return self.db.query(ContactTypeModel).where(ContactTypeModel.id == id).first()
    
    # get contact type code function
    def getbycode(self, code: str) -> ContactTypeModel:
        return self.db.query(ContactTypeModel).where(ContactTypeModel.code == code).first()
    
    # get contact type name function
    def getbyname(self, name: str) -> ContactTypeModel:
        return self.db.query(ContactTypeModel).where(func.lower(ContactTypeModel.name) == name.lower()).first()
    
    # create contact type function
    def create(self, data: List[CreateContactType]) -> List[CreateContactType]:
        self.db.execute(insert(ContactTypeModel), encoders.jsonable_encoder(data))
        self.db.commit()
        return data

    # update contact type function
    def update(self, data: ContactTypeModel) -> ContactTypeModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete contact type function
    def delete(self, contact: ContactTypeModel) -> None:
        self.db.delete(contact)
        self.db.commit()