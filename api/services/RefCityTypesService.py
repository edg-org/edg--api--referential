from typing import List, Optional

from fastapi import Depends
from api.models.RefCityTypesModel import RefCityTypes
from api.repositories.RefCitiesRepository import RefCitiesRepository
from api.repositories.RefCityTypesRepository import RefCityTypesRepository
from api.schemas.pydantic.RefCityTypesSchema import (RefCityTypesSchema, RefCityTypesCreateSchema, EXAMPLE, RefCityTypesUpdateSchema, EXAMPLE1)

class RefCityTypesService:
    refCityTypes: RefCityTypesRepository
    def __init__(self, refCityTypes: RefCityTypesRepository = Depends()) -> None:
        self.refCityTypes = refCityTypes

    def create(self, city_types_body: RefCityTypesCreateSchema):
    # def create(self, city_types_body: RefCityTypesCreateSchema) -> RefCityTypesSchema:
        return self.refCityTypes.create(city_types_body)

    def get(self, id: int) -> RefCityTypes:
        return self.refCityTypes.get(id)

    def list(self, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[RefCityTypes]:
        return self.refCityTypes.list(skip, limit)

    def update(self, city_types_body: RefCityTypesUpdateSchema) -> RefCityTypes:
        ref_city_type = self.refCityTypes.get(city_types_body.id)
        return self.refCityTypes.update(city_types_body)

    # def delete(self, id: int) -> RefCityTypes:
    def delete(self, id: int):
        ref_city_type = self.refCityTypes.get(id, True)
        return self.refCityTypes.delete(id)

    def retaure(self, id: int):
        ref_city_type = self.refCityTypes.get(id, False)
        return self.refCityTypes.delete(id, True)

    def delete_signature(self, id : int, signature : str):
        ref_city_type = self.refCityTypes.get_id_and_signature(id, signature)
        return self.refCityTypes.delete_signature(id, signature)

    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None) :
        return self.refCityTypes.get_items(id, code, signature)







