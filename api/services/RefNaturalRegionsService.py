from typing import List, Optional

from fastapi import Depends
from api.models.RefNaturalRegionsModel import RefNaturalRegions

from api.repositories.RefNaturalRegionsRepository import RefNaturalRegionsRepository
from api.schemas.pydantic.RefNaturalRegionsSchema import RefNaturalRegionsSchema,RefNaturalRegionsCreateSchema,RefNaturalRegionsUpdateSchema


class RefNaturalRegionsService:
    refNaturalRegions: RefNaturalRegionsRepository
    def __init__(self, refNaturalRegions: RefNaturalRegionsRepository = Depends()) -> None:
        self.refNaturalRegions = refNaturalRegions

    def create(self, natural_region_body: RefNaturalRegionsCreateSchema):
    # def create(self, natural_region_body: RefNaturalRegionsCreateSchema) -> RefNaturalRegionsSchema:
        return self.refNaturalRegions.create(natural_region_body)

    def get(self, id: int) -> RefNaturalRegions:
        return self.refNaturalRegions.get(id, is_log = True)

    def list(self, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[RefNaturalRegions]:
        return self.refNaturalRegions.list(skip, limit)

    def update(self, natural_region_body: RefNaturalRegionsUpdateSchema) -> RefNaturalRegions:
        ref_natural_region = self.refNaturalRegions.get(natural_region_body.id)
        return self.refNaturalRegions.update(natural_region_body)

    # def delete(self, id: int) -> RefNaturalRegions:
    def delete(self, id: int):
        ref_natural_region = self.refNaturalRegions.get(id, True)
        return self.refNaturalRegions.delete(id)

    def retaure(self, id: int):
        ref_natural_region = self.refNaturalRegions.get(id, False)
        return self.refNaturalRegions.delete(id, True)

    def delete_signature(self, id : int, signature : str):
        ref_natural_region = self.refNaturalRegions.get_id_and_signature(id, signature)
        return self.refNaturalRegions.delete_signature(id, signature)

    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None) :
        return self.refNaturalRegions.get_items(id, code, signature)








