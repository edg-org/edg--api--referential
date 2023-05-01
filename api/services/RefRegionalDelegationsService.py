from typing import List, Optional

from fastapi import Depends
from api.models.RefRegionalDelegationsModel import RefRegionalDelegations

from api.repositories.RefRegionalDelegationsRepository import RefRegionalDelegationsRepository
from api.schemas.pydantic.RefRegionalDelegationsSchema import RefRegionalDelegationsSchema,RefRegionalDelegationsCreateSchema,RefRegionalDelegationsUpdateSchema


class RefRegionalDelegationsService:
    refRegionalDelegations: RefRegionalDelegationsRepository
    def __init__(self, refRegionalDelegations: RefRegionalDelegationsRepository = Depends()) -> None:
        self.refRegionalDelegations = refRegionalDelegations

    def create(self, natural_region_body: RefRegionalDelegationsCreateSchema):
    # def create(self, natural_region_body: RefRegionalDelegationsCreateSchema) -> RefRegionalDelegationsSchema:
        return self.refRegionalDelegations.create(natural_region_body)

    def get(self, id: int) -> RefRegionalDelegations:
        return self.refRegionalDelegations.get(id)

    def list(self, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[RefRegionalDelegations]:
        return self.refRegionalDelegations.list(skip, limit)

    def update(self, natural_region_body: RefRegionalDelegationsUpdateSchema) -> RefRegionalDelegations:
        ref_natural_region = self.refRegionalDelegations.get(natural_region_body.id)
        return self.refRegionalDelegations.update(natural_region_body)

    # def delete(self, id: int) -> RefRegionalDelegations:
    def delete(self, id: int):
        ref_natural_region = self.refRegionalDelegations.get(id, True)
        return self.refRegionalDelegations.delete(id)

    def retaure(self, id: int):
        ref_natural_region = self.refRegionalDelegations.get(id, False)
        return self.refRegionalDelegations.delete(id, True)

    def delete_signature(self, id : int, signature : str):
        ref_natural_region = self.refRegionalDelegations.get_id_and_signature(id, signature)
        return self.refRegionalDelegations.delete_signature(id, signature)


    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None) :
        return self.refRegionalDelegations.get_items(id, code, signature)








