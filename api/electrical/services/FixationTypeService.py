from typing import List
from api.tools.Helper import build_log
from fastapi.encoders import jsonable_encoder
from api.logs.repositories.LogRepo import LogRepo
from fastapi import Depends, HTTPException, status
from api.electrical.models.FixationTypeModel import FixationTypeModel
from api.electrical.repositories.FixationTypeRepo import FixationTypeRepo
from api.electrical.schemas.FixationTypeSchema import (
    FixationTypeUpdate,
    CreateFixationType
)

#
class FixationTypeService:
    log: LogRepo
    fixationtype: FixationTypeRepo

    def __init__(
        self, 
        log: LogRepo = Depends(),
        fixationtype: FixationTypeRepo = Depends()
    ) -> None:
        self.log = log
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
    async def getbycode(self, code: str) -> FixationTypeModel:
        return self.fixationtype.getbycode(code=code)

    # get fixation type by name function
    async def getbyname(self, name: str) -> FixationTypeModel:
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
        old_data = jsonable_encoder(self.fixationtype.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fixation Type not found",
            )

        current_data = jsonable_encoder(self.fixationtype.update(code=code, data=data.dict()))
        logs = [build_log(f"/fixationtypes/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # delete fixation type function
    async def delete(self, code: int) -> None:
        data = self.fixationtype.getbycode(code=code)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fixation Type not found",
            )

        self.fixationtype.delete(data)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Fixation Type deleted",
        )