from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert, func
from fastapi import Depends, encoders
from api.configs.Database import get_db
from api.electrical.models.TransformerModel import (
    TransformerModel,
)
from api.electrical.schemas.TransformerSchema import (
    CreateTransformer,
)


class TransformerRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        return self.db.query(
            func.max(TransformerModel.code)
        ).one()[0]

    # get all transformers function
    def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[TransformerModel]:
        return (
            self.db.query(TransformerModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get transformer by id function
    def get(self, id: int) -> TransformerModel:
        return (
            self.db.query(TransformerModel)
            .where(TransformerModel.id == id)
            .first()
        )

    # get transformer number function
    def getbynumber(self, number: str) -> TransformerModel:
        return (
            self.db.query(TransformerModel)
            .where(
                TransformerModel.transformer_number
                == number
            )
            .first()
        )
  
    def getbyname(self, name: str) -> TransformerModel:
        return (
            self.db.query(TransformerModel)
            .where(
                TransformerModel.infos['name'] == name               
            )
            .first()            
        )        

    # create transformer function
    def create(
        self, data: List[CreateTransformer]
    ) -> List[CreateTransformer]:
        self.db.execute(
            insert(TransformerModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update transformer function
    def update(
        self, data: TransformerModel
    ) -> TransformerModel:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    # delete transformer function
    def delete(self, meter: TransformerModel) -> None:
        self.db.delete(meter)
        self.db.commit()

    # get transformer code function
    def getbycode(self, code: str) -> TransformerModel:
        return (
            self.db.query(TransformerModel)
            .where(
                func.lower(TransformerModel.code)
                == code.lower()
            )
            .first()
        )
    # get transformer_number function
    def getbytransformernumber(self, number: str) -> TransformerModel:
        return (
            self.db.query(TransformerModel)
            .where(
                func.lower(TransformerModel.transformer_number)
                == number.lower()
            )
            .first()
        )