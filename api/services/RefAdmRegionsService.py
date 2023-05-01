from typing import List, Optional

from fastapi import Depends
from api.models.RefNaturalRegionsModel import RefNaturalRegions
from api.models.RefAdmRegionsModel import RefAdmRegions
from api.repositories.RefAdmRegionsRepository import RefAdmRegionsRepository
from api.repositories.RefNaturalRegionsRepository import RefNaturalRegionsRepository

from api.schemas.pydantic.RefNaturalRegionsSchema import RefNaturalRegionsSchema, RefNaturalRegionsCreateSchema
from api.schemas.pydantic.RefAdmRegionsSchema import (RefAdmRegionsSchema, RefAdmRegionsCreateSchema, EXAMPLE,
RefAdmRegionsUpdateSchema, EXAMPLE1, RefAdmRegionsSearchSchema)

class RefAdmRegionsService:
    refNaturalRegions: RefNaturalRegionsRepository
    refAdmRegions: RefAdmRegionsRepository
    def __init__(self, refNaturalRegions: RefNaturalRegionsRepository = Depends(), refAdmRegions: RefAdmRegionsRepository = Depends()) -> None:
        self.refNaturalRegions = refNaturalRegions
        self.refAdmRegions = refAdmRegions

    def create(self, adm_region_body: RefAdmRegionsCreateSchema):
    # def create(self, adm_region_body: RefAdmRegionsCreateSchema) -> RefAdmRegionsSchema:
        return self.refAdmRegions.create(adm_region_body)

    def get(self, id: int) -> RefAdmRegions:
        return self.refAdmRegions.get(id)

    def list(self, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[RefAdmRegions]:
        return self.refAdmRegions.list(skip, limit)

    # def update(self, id: int, infos: dict, natural_region_id : int) -> RefAdmRegions:
    def update(self, adm_region_body: RefAdmRegionsUpdateSchema) :
        ref_adm_region = self.refAdmRegions.get(adm_region_body.id)
        return self.refAdmRegions.update(adm_region_body)

    # def delete(self, id: int) -> RefAdmRegions:
    def delete(self, id: int):
        ref_adm_region = self.refAdmRegions.get(id, True)
        return self.refAdmRegions.delete(id)

    def retaure(self, id: int):
        ref_adm_region = self.refAdmRegions.get(id, False)
        return self.refAdmRegions.delete(id, True)

    def delete_signature(self, id : int, signature : str):
        ref_adm_region = self.refAdmRegions.get_id_and_signature(id, signature)
        return self.refAdmRegions.delete_signature(id, signature)

    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None) :
        # return self.refAdmRegions.get_items(RefAdmRegionsSearchSchema(id = id, code = code, signature = signature))
        return self.refAdmRegions.get_items(id, code, signature)
        # return self.refAdmRegions.get_items({"id" : id,"code" : code,"signature" : signature})
        # return self.refAdmRegions.get_items(adm_region_body)
