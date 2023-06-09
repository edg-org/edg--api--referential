from typing import List
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from api.logs.repositories.LogRepo import LogRepo
from fastapi import Depends, HTTPException, status
from api.electrical.models.MeterTypeModel import MeterTypeModel
from api.electrical.repositories.MeterTypeRepo import MeterTypeRepo
from api.electrical.schemas.MeterTypeSchema import (
    MeterTypeUpdate,
    CreateMeterType
)


#
class MeterTypeService:
    log: LogRepo
    metertype: MeterTypeRepo

    def __init__(
        self, 
        log: LogRepo = Depends(),
        metertype: MeterTypeRepo = Depends()
    ) -> None:
        self.log = log
        self.metertype = metertype

    # get all meter types function
    async def list(self, start: int = 0, size: int = 100) -> List[MeterTypeModel]:
        return self.metertype.list(start=start, size=size)

    # get meter type by id function
    async def get(self, id: int) -> MeterTypeModel:
        return self.metertype.get(id=id)

    # get meter type by code function
    async def getbycode(self, code: str) -> MeterTypeModel:
        return self.metertype.getbycode(code=code)

    # get meter type by name function
    async def getbyname(self, name: str) -> MeterTypeModel:
        return self.metertype.getbyname(name=name)

    # create meter type function
    async def create(self, data: List[CreateMeterType]) -> List[CreateMeterType]:
        for item in data:
            metertype = self.metertype.getbycode(code=item.code)
            if metertype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Meter Type already registered with code {item.code}",
                )

            metertype = self.metertype.getbyname(name=item.name)
            if metertype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Meter Type already registered with name {item.name}",
                )

        return self.metertype.create(data=data)

    # update meter type function
    async def update(self, code: int, data: MeterTypeUpdate) -> MeterTypeUpdate:
        old_data = jsonable_encoder(self.metertype.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meter Type not found",
            )

        current_data = jsonable_encoder(self.metertype.update(code=code, data=data.dict()))
        logs = [Helper.build_log(f"/metertypes/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # delete meter type function
    async def delete(self, type: MeterTypeModel) -> None:
        metertype = self.metertype.get(id=id)
        if metertype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meter Type not found",
            )

        self.metertype.update(type)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Meter Type deleted",
        )
