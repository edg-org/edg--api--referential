from typing import List, Optional

from fastapi import Depends
from api.models.RefMicroServicesModel import RefMicroServices

from api.repositories.RefMicroServicesRepository import RefMicroServicesRepository
from api.schemas.pydantic.RefMicroServicesSchema import RefMicroServicesSchema,RefMicroServicesCreateSchema,RefMicroServicesUpdateSchema


class RefMicroServicesService:
    refMicroServices: RefMicroServicesRepository
    def __init__(self, refMicroServices: RefMicroServicesRepository = Depends()) -> None:
        self.refMicroServices = refMicroServices

    def create(self, micro_service_body: RefMicroServicesCreateSchema):
    # def create(self, micro_service_body: RefMicroServicesCreateSchema) -> RefMicroServicesSchema:
        return self.refMicroServices.create(micro_service_body)

    def get(self, id: int) -> RefMicroServices:
        return self.refMicroServices.get(id)

    def list(self, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[RefMicroServices]:
        return self.refMicroServices.list(skip, limit)

    def update(self, micro_service_body: RefMicroServicesUpdateSchema) -> RefMicroServices:
        ref_micro_service = self.refMicroServices.get(micro_service_body.id)
        return self.refMicroServices.update(micro_service_body)

    # def delete(self, id: int) -> RefMicroServices:
    def delete(self, id: int):
        ref_micro_service = self.refMicroServices.get(id, True)
        return self.refMicroServices.delete(id)

    def retaure(self, id: int):
        ref_micro_service = self.refMicroServices.get(id, False)
        return self.refMicroServices.delete(id, True)

    def delete_signature(self, id : int, signature : str):
        ref_micro_service = self.refMicroServices.get_id_and_signature(id, signature)
        return self.refMicroServices.delete_signature(id, signature)


    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None) :
        return self.refMicroServices.get_items(id, code, signature)








