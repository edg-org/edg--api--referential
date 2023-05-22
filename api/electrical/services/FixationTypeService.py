from typing import List
from fastapi import Depends, HTTPException, status
from api.electrical.models.FixationTypeModel import FixationTypeModel
from api.electrical.repositories.FixationTypeRepo import FixationTypeRepo
from api.electrical.schemas.FixationTypeSchema import (
    FixationTypeBase,
    FixationTypeUpdate,
    CreateFixationType
)

#
class FixationTypeService:
    fixationtype: FixationTypeRepo

    def __init__(
        self, fixationtype: FixationTypeRepo = Depends()
    ) -> None:
        self.fixationtype = fixationtype

    # get all fixation types function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[FixationTypeModel]:
        return self.fixationtype.list(skip=skip, limit=limit)

    # get fixation type by id function
    async def get(self, id: int) -> FixationTypeModel:
        return self.fixationtype.get(id=id)

    # get fixation type by code function
    async def getbycode(self, code: str) -> FixationTypeBase:
        return self.fixationtype.getbycode(code=code)

    # get fixation type by name function
    async def getbyname(self, name: str) -> FixationTypeBase:
        return self.fixationtype.getbyname(name=name)

    # create fixation type function
    async def create(self, data: List[CreateFixationType]) -> List[CreateFixationType]:
        for item in data:
            fixationtype = self.fixationtype.getbycode(code=item.code)
            if fixationtype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Fixation Type already registered with code " + str(item.code),
                )

            fixationtype = self.fixationtype.getbyname(name=item.name)
            if fixationtype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Fixation Type already registered with name " + item.name,
                )
        return self.fixationtype.create(data=data)

    # update fixation type function
    async def update(self, code: int, data: FixationTypeUpdate) -> FixationTypeUpdate:
        fixationtype = self.fixationtype.getbycode(code=code)
        if fixationtype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fixation Type not found",
            )

        fixationtypedict = data.dict(exclude_unset=True)
        for key, val in fixationtypedict.items():
            setattr(fixationtype, key, val)
        return self.fixationtype.update(fixationtype)

    # delete fixation type function
    async def delete(self, type: FixationTypeModel) -> None:
        fixationtype = self.fixationtype.get(id=id)
        if fixationtype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fixation Type not found",
            )

        self.fixationtype.update(type)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Fixation Type deleted",
        )