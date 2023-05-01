from typing import List, Optional

from fastapi import Depends
from api.models.RefAreasModel import RefAreas
from api.repositories.RefCitiesRepository import RefCitiesRepository
from api.repositories.RefAreasRepository import RefAreasRepository
from api.schemas.pydantic.RefAreasSchema import RefAreasSchema, RefAreasCreateSchema, EXAMPLE, RefAreasUpdateSchema, EXAMPLE1

class RefAreasService:
    refCities: RefCitiesRepository
    refAreas: RefAreasRepository
    def __init__(self, refCities: RefCitiesRepository = Depends(), refAreas: RefAreasRepository = Depends()) -> None:
        self.refCities = refCities
        self.refAreas = refAreas

    def create(self, areas_body: RefAreasCreateSchema):
    # def create(self, areas_body: RefAreasCreateSchema) -> RefAreasSchema:
        return self.refAreas.create(areas_body)

    def get(self, id: int) -> RefAreas:
        return self.refAreas.get(id)

    def list(self, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[RefAreas]:
        return self.refAreas.list(skip, limit)

    def update(self, areas_body: RefAreasUpdateSchema) -> RefAreas:
        ref_area = self.refAreas.get(areas_body.id)
        return self.refAreas.update(areas_body)

    # def delete(self, id: int) -> RefAreas:
    def delete(self, id: int):
        ref_area = self.refAreas.get(id, True)
        return self.refAreas.delete(id)

    def retaure(self, id: int):
        ref_area = self.refAreas.get(id, False)
        return self.refAreas.delete(id, True)

    def delete_signature(self, id : int, signature : str):
        ref_area = self.refAreas.get_id_and_signature(id, signature)
        return self.refAreas.delete_signature(id, signature)

    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None) :
        return self.refAreas.get_items(id, code, signature)

