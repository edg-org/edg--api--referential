from typing import List, Optional

from fastapi import Depends
from api.models.RefNaturalRegionsModel import RefNaturalRegions
from api.models.RefPrefecturesModel import RefPrefectures
from api.repositories.RefPrefecturesRepository import RefPrefecturesRepository
from api.repositories.RefNaturalRegionsRepository import RefNaturalRegionsRepository

from api.schemas.pydantic.RefPrefecturesSchema import (RefPrefecturesSchema, RefPrefecturesCreateSchema, EXAMPLE,
RefPrefecturesUpdateSchema, EXAMPLE1)

class RefPrefecturesService:
    refNaturalRegions: RefNaturalRegionsRepository
    refPrefectures: RefPrefecturesRepository
    def __init__(self, refNaturalRegions: RefNaturalRegionsRepository = Depends(), refPrefectures: RefPrefecturesRepository = Depends()) -> None:
        self.refNaturalRegions = refNaturalRegions
        self.refPrefectures = refPrefectures

    def create(self, prefecture_body: RefPrefecturesCreateSchema):
    # def create(self, prefecture_body: RefPrefecturesCreateSchema) -> RefPrefecturesSchema:
        return self.refPrefectures.create(prefecture_body)

    def get(self, id: int) -> RefPrefectures:
        return self.refPrefectures.get(id)

    def list(self, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[RefPrefectures]:
        return self.refPrefectures.list(skip, limit)

    def update(self, prefecture_body: RefPrefecturesUpdateSchema) -> RefPrefectures:
        ref_prefecture = self.refPrefectures.get(prefecture_body.id)
        return self.refPrefectures.update(prefecture_body)

    # def delete(self, id: int) -> RefPrefectures:
    def delete(self, id: int):
        ref_prefecture = self.refPrefectures.get(id, True)
        return self.refPrefectures.delete(id)

    def retaure(self, id: int):
        ref_prefecture = self.refPrefectures.get(id, False)
        return self.refPrefectures.delete(id, True)

    def delete_signature(self, id : int, signature : str):
        ref_prefecture = self.refPrefectures.get_id_and_signature(id, signature)
        return self.refPrefectures.delete_signature(id, signature)



    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None) :
        return self.refPrefectures.get_items(id, code, signature)







