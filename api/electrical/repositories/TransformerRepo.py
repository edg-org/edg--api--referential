from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, encoders
from api.configs.Database import get_db
from sqlalchemy import insert, update, func, or_, and_, null, select
from api.electrical.models.TransformerModel import TransformerModel
from api.electrical.schemas.TransformerSchema import CreateTransformer

class TransformerRepo:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db)
    ) -> None:
        self.db = db

    # get max code
    def maxcode(self) -> int:
        codemax = self.db.query(
            func.max(TransformerModel.code)
        ).one()[0]
        return 0 if codemax is None else codemax

    # get max id of area by city
    def maxcodebycity(self, city_code: int) -> int:
        codemax = (
            self.db.query(func.max(TransformerModel.transformer_code))
            .where(
                and_(
                    TransformerModel.infos["city_code"] == city_code,
                    TransformerModel.infos["transformer_serial_number"] == null()
                )
            ).one()[0]
        )
        return 0 if codemax is None else codemax

    # get all transformers function
    def list(self, skip: int = 0, limit: int = 100) -> List[TransformerModel]:
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

    # get transformer code function
    def getbycode(self, code: int) -> TransformerModel:
        return (
            self.db.query(TransformerModel)
            .where(TransformerModel.transformer_code == code)
            .first()
        )

    # get transformer id by code function
    def getidbycode(self, code: int) -> int:
        return (
            self.db.query(TransformerModel.id)
            .where(TransformerModel.transformer_code == code)
            .one()[0]
        )

    # get transformer name function
    def getbyname(self, name: str) -> TransformerModel:
        return (
            self.db.query(TransformerModel)
            .where(func.lower(TransformerModel.infos["name"]) == name.lower())
            .first()
        )

    # count total rows of transformer by code
    def countbycode(self, code: str) -> int:
        return (
            self.db.query(TransformerModel)
            .where(TransformerModel.transformer_code == code)
            .count()
        )

    # check trasnformer name in the place function
    def checktransformername(self, place_code: int, name: str) -> int:
        return (
            self.db.query(func.count(TransformerModel.id))
            .where(
                and_(
                    or_(
                        TransformerModel.infos["city_code"] == place_code,
                        TransformerModel.infos["area_code"] == place_code,
                    ),
                    func.lower(func.json_unquote(TransformerModel.infos["name"])) == name.lower()
                )
            ).one()[0]
        )

    # create transformer function
    def create(self, data: List[CreateTransformer]) -> List[CreateTransformer]:
        self.db.execute(
            insert(TransformerModel),
            encoders.jsonable_encoder(data),
        )
        self.db.commit()
        return data

    # update transformer function
    def update(self, code: int, data: CreateTransformer) -> TransformerModel:
        self.db.execute(
            update(TransformerModel)
            .where(TransformerModel.transformer_code == code)
            .values(**data)
        )
        self.db.commit()
        return self.getbycode(code=code)

    # delete transformer function
    def delete(self, meter: TransformerModel) -> None:
        self.db.delete(meter)
        self.db.commit()
    def verif_duplicate(self, name: str, req: str = "True") -> [TransformerModel]:
        stmt = (
            select(TransformerModel)
            .filter(TransformerModel.name.ilike(name))
            .filter(eval(req))
        )
        return self.db.scalars(stmt).all()