from typing import List, Optional

from fastapi import Depends
from api.models.RefNaturalRegionsModel import RefNaturalRegions
from api.models.RefPrefecturesModel import RefPrefectures
from api.models.RefCitiesModel import RefCities
from api.repositories.RefPrefecturesRepository import RefPrefecturesRepository
from api.repositories.RefNaturalRegionsRepository import RefNaturalRegionsRepository
from api.repositories.RefCitiesRepository import RefCitiesRepository

from api.schemas.pydantic.RefNaturalRegionsSchema import RefNaturalRegionsSchema, RefNaturalRegionsCreateSchema
from api.schemas.pydantic.RefPrefecturesSchema import RefPrefecturesSchema, RefPrefecturesCreateSchema
from api.schemas.pydantic.RefCitiesSchema import (RefCitiesSchema, RefCitiesCreateSchema, EXAMPLE, RefCitiesUpdateSchema,
EXAMPLE1)

class RefCitiesService:
    refPrefectures: RefPrefecturesRepository
    refCities: RefCitiesRepository
    def __init__(self, refPrefectures: RefNaturalRegionsRepository = Depends(), refCities: RefCitiesRepository = Depends()) -> None:
        self.refPrefectures = refPrefectures
        self.refCities = refCities

    def create(self, cities_body: RefCitiesCreateSchema):
    # def create(self, cities_body: RefCitiesCreateSchema) -> RefCitiesSchema:
        return self.refCities.create(cities_body)

    def get(self, id: int) -> RefCities:
        return self.refCities.get(id)

    def list(self, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[RefCities]:
        return self.refCities.list(skip, limit)

    def update(self, cities_body: RefCitiesUpdateSchema) -> RefCities:
        ref_citie = self.refCities.get(cities_body.id)
        return self.refCities.update(cities_body)

    # def delete(self, id: int) -> RefCities:
    def delete(self, id: int):
        ref_citie = self.refCities.get(id, True)
        return self.refCities.delete(id)

    def retaure(self, id: int):
        ref_citie = self.refCities.get(id, False)
        return self.refCities.delete(id, True)

    def delete_signature(self, id : int, signature : str):
        ref_citie = self.refCities.get_id_and_signature(id, signature)
        return self.refCities.delete_signature(id, signature)

    def get_code(self, code: str) -> RefCities:
        return self.refCities.get_code(code)


    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None) :
        return self.refCities.get_items(id, code, signature)




