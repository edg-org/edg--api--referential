from typing import List, Optional

from fastapi import Depends
from api.models.RefTypeAreasModel import RefTypeAreas
from api.repositories.RefCitiesRepository import RefCitiesRepository
from api.repositories.RefTypeAreasRepository import RefTypeAreasRepository
from api.schemas.pydantic.RefTypeAreasSchema import (RefTypeAreasSchema, RefTypeAreasCreateSchema, EXAMPLE, 
    RefTypeAreasUpdateSchema, EXAMPLE1)

class RefTypeAreasService:
    refTypeAreas: RefTypeAreasRepository
    def __init__(self, refTypeAreas: RefTypeAreasRepository = Depends()) -> None:
        self.refTypeAreas = refTypeAreas

    def create(self, type_areas_body: RefTypeAreasCreateSchema):
    # def create(self, type_areas_body: RefTypeAreasCreateSchema) -> RefTypeAreasSchema:
        return self.refTypeAreas.create(type_areas_body)

    def get(self, id: int) -> RefTypeAreas:
        return self.refTypeAreas.get(id)

    def list(self, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[RefTypeAreas]:
        return self.refTypeAreas.list(skip, limit)

    def update(self, type_areas_body: RefTypeAreasUpdateSchema) -> RefTypeAreas:
        ref_type_area = self.refTypeAreas.get(type_areas_body.id)
        return self.refTypeAreas.update(type_areas_body)

    # def delete(self, id: int) -> RefTypeAreas:
    def delete(self, id: int):
        ref_type_area = self.refTypeAreas.get(id, True)
        return self.refTypeAreas.delete(id)

    def retaure(self, id: int):
        ref_type_area = self.refTypeAreas.get(id, False)
        return self.refTypeAreas.delete(id, True)

    def delete_signature(self, id : int, signature : str):
        ref_type_area = self.refTypeAreas.get_id_and_signature(id, signature)
        return self.refTypeAreas.delete_signature(id, signature)


    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None) :
        return self.refTypeAreas.get_items(id, code, signature)







