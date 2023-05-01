from typing import List, Optional

from fastapi import Depends
from api.models.RefCityLevelsModel import RefCityLevels
from api.repositories.RefCitiesRepository import RefCitiesRepository
from api.repositories.RefCityLevelsRepository import RefCityLevelsRepository
from api.schemas.pydantic.RefCityLevelsSchema import (RefCityLevelsSchema, RefCityLevelsCreateSchema, EXAMPLE, 
    RefCityLevelsUpdateSchema, EXAMPLE1)

class RefCityLevelsService:
    refCityLevels: RefCityLevelsRepository
    def __init__(self, refCityLevels: RefCityLevelsRepository = Depends()) -> None:
        self.refCityLevels = refCityLevels

    def create(self, city_levels_body: RefCityLevelsCreateSchema):
    # def create(self, city_levels_body: RefCityLevelsCreateSchema) -> RefCityLevelsSchema:
        return self.refCityLevels.create(city_levels_body)

    def get(self, id: int) -> RefCityLevels:
        return self.refCityLevels.get(id)

    def list(self, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[RefCityLevels]:
        return self.refCityLevels.list(skip, limit)

    def update(self, city_levels_body: RefCityLevelsUpdateSchema) -> RefCityLevels:
        ref_city_level = self.refCityLevels.get(city_levels_body.id)
        return self.refCityLevels.update(city_levels_body)

    # def delete(self, id: int) -> RefCityLevels:
    def delete(self, id: int):
        ref_city_level = self.refCityLevels.get(id, True)
        return self.refCityLevels.delete(id)

    def retaure(self, id: int):
        ref_city_level = self.refCityLevels.get(id, False)
        return self.refCityLevels.delete(id, True)

    def delete_signature(self, id : int, signature : str):
        ref_city_level = self.refCityLevels.get_id_and_signature(id, signature)
        return self.refCityLevels.delete_signature(id, signature)


    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None) :
        return self.refCityLevels.get_items(id, code, signature)







