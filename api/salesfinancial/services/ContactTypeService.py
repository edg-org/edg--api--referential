from typing import List
from fastapi import Depends, HTTPException, status
from api.salesfinancial.models.ContactTypeModel import ContactTypeModel
from api.salesfinancial.repositories.ContactTypeRepo import ContactTypeRepo
from api.salesfinancial.schemas.ContactTypeSchema import CreateContactType
from fastapi.encoders import jsonable_encoder
from api.tools.Helper import build_log
from api.logs.repositories.LogRepo import LogRepo

class ContactTypeService:
    contacttype: ContactTypeRepo
    log: LogRepo
    def __init__(
        self, contacttype: ContactTypeRepo = Depends(), log: LogRepo = Depends(),
    ) -> None:
        self.contacttype = contacttype
        self.log = log

    # get all contact types function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[ContactTypeModel]:
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
                    detail="Contact Type already registered with code "
                    + str(item.code),
                )

            contacttype = self.contacttype.getbyname(name=item.name)
            if contacttype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Contact Type already registered with name "
                    + item.name,
                )

        return self.contacttype.create(data=data)

    # # update contact type function
    # async def update(self, code: int, data: CreateContactType) -> ContactTypeModel:
    #     contacttype = self.contacttype.getbycode(code=code)
    #     if contacttype is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail="Contact Type not found",
    #         )
    #
    #     typedict = data.dict(exclude_unset=True)
    #     for key, val in typedict.items():
    #         setattr(contacttype, key, val)
    #     return self.contacttype.update(contacttype)

    async def update(self, code: int, data: CreateContactType) -> ContactTypeModel:
        old_data = jsonable_encoder(self.contacttype.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact Type not found",
            )

        verif = self.contacttype.verif_duplicate(data.name, "ContactTypeModel.id != " + str(old_data['id']))
        if len(verif) != 0:
            raise HTTPException(status_code=405, detail={"msg": "Duplicates are not possible", "name": data.name})

        current_data = jsonable_encoder(self.contacttype.update(code=code, data=data.dict()))
        logs = [await build_log(f"/contacttype/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        self.log.create(logs)
        return current_data

    # delete contact type %function
    async def delete(self, contact: ContactTypeModel) -> None:
        code = 0
        contacttype = self.contacttype.getbycode(code=code)
        if contacttype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact Type not found",
            )

        self.contacttype.update(contact)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Contact Type deleted",
        )
