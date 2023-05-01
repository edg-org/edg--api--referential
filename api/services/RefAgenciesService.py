from typing import List, Optional

from fastapi import Depends
from api.models.RefAgenciesModel import RefAgencies
from api.repositories.RefCitiesRepository import RefCitiesRepository
from api.repositories.RefAgenciesRepository import RefAgenciesRepository
from api.schemas.pydantic.RefAgenciesSchema import (RefAgenciesSchema, RefAgenciesCreateSchema, EXAMPLE, RefAgenciesUpdateSchema,
EXAMPLE1)

class RefAgenciesService:
    refCities: RefCitiesRepository
    refAgencies: RefAgenciesRepository
    def __init__(self, refCities: RefCitiesRepository = Depends(), refAgencies: RefAgenciesRepository = Depends()) -> None:
        self.refCities = refCities
        self.refAgencies = refAgencies

    def create(self, agencies_body: RefAgenciesCreateSchema):
    # def create(self, agencies_body: RefAgenciesCreateSchema) -> RefAgenciesSchema:
        return self.refAgencies.create(agencies_body)

    def get(self, id: int) -> RefAgencies:
        return self.refAgencies.get(id)

    def list(self, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[RefAgencies]:
        return self.refAgencies.list(skip, limit)

    def update(self, agencies_body: RefAgenciesUpdateSchema) -> RefAgencies:
        ref_agencie = self.refAgencies.get(agencies_body.id)
        return self.refAgencies.update(agencies_body)

    # def delete(self, id: int) -> RefAgencies:
    def delete(self, id: int):
        ref_agencie = self.refAgencies.get(id, True)
        return self.refAgencies.delete(id)

    def retaure(self, id: int):
        ref_agencie = self.refAgencies.get(id, False)
        return self.refAgencies.delete(id, True)

    def delete_signature(self, id : int, signature : str):
        ref_agencie = self.refAgencies.get_id_and_signature(id, signature)
        return self.refAgencies.delete_signature(id, signature)

    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None) :
        return self.refAgencies.get_items(id, code, signature)






