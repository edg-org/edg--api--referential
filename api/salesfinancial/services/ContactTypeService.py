from typing import List
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from api.logs.services.LogService import LogService
from api.salesfinancial.models.ContactTypeModel import ContactTypeModel
from api.salesfinancial.repositories.ContactTypeRepo import ContactTypeRepo
from api.salesfinancial.schemas.ContactTypeSchema import CreateContactType

class ContactTypeService:
    log: LogService = Depends()
    contacttype: ContactTypeRepo

    def __init__(
        self, 
        log: LogService = Depends(),
        contacttype: ContactTypeRepo = Depends()
    ) -> None:
        self.log = log
        self.contacttype = contacttype

    # get all contact types function
    async def list(self, skip: int = 0, limit: int = 100) -> List[ContactTypeModel]:
        return self.contacttype.list(skip=skip, limit=limit)

    # get contact type by id function
    async def get(self, id: int) -> ContactTypeModel:
        return self.contacttype.get(id=id)

    # get contact type by code function
    async def getbycode(self, code: str) -> ContactTypeModel:
        return self.contacttype.getbycode(code=code)

    # get contact type by name function
    async def getbyname(self, name: str) -> ContactTypeModel:
        return self.contacttype.getbyname(name=name)

    # create contact type function
    async def create(self, data: List[CreateContactType]) -> List[CreateContactType]:
        for item in data:
            contacttype = self.contacttype.getbycode(code=item.code)
            if contacttype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Contact Type already registered with code {item.code}"
                )

            contacttype = self.contacttype.getbyname(name=item.name)
            if contacttype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Contact Type already registered with name {item.name}"
                )

        return self.contacttype.create(data=data)

    # update contact type function
    async def update(self, code: int, tokendata:dict, data: CreateContactType) -> ContactTypeModel:
        old_data = jsonable_encoder(self.contacttype.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact Type not found",
            )

        current_data = jsonable_encoder(self.contacttype.update(code, data=data.dict()))
        logs = [await Helper.build_log(f"/contacttypes/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # delete contact type %function
    async def delete(self, code: int) -> None:
        data = self.contacttype.getbycode(code=code)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact Type not found",
            )

        self.contacttype.delete(data)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Contact Type deleted",
        )