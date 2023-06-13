from typing import List
from api.tools.Helper import build_log
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from api.logs.services.LogService import LogService
from api.electrical.models.VoltageTypeModel import VoltageTypeModel
from api.electrical.repositories.VoltageTypeRepo import VoltageTypeRepo
from api.electrical.schemas.VoltageTypeSchema import (
    VoltageTypeUpdate,
    CreateVoltageType
)

#
class VoltageTypeService:
    voltagetype: VoltageTypeRepo
    log: LogService

    def __init__(
        self, 
        log: LogService = Depends(),
        voltagetype: VoltageTypeRepo = Depends()
    ) -> None:
        self.log = log
        self.voltagetype = voltagetype

    # get all voltage types function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[VoltageTypeModel]:
        return self.voltagetype.list(skip=skip, limit=limit)

    # get voltage type by id function
    async def get(self, id: int) -> VoltageTypeModel:
        return self.voltagetype.get(id=id)

    # get voltage type by code function
    async def getbycode(self, code: str) -> VoltageTypeModel:
        return self.voltagetype.getbycode(code=code)

    # get voltage type by name function
    async def getbyname(self, name: str) -> VoltageTypeModel:
        return self.voltagetype.getbyname(name=name)

    # create voltage type function
    async def create(self, data: List[CreateVoltageType]) -> List[CreateVoltageType]:
        for item in data:
            voltagetype = self.voltagetype.getbycode(code=item.code)
            if voltagetype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Voltage Type already registered with code {item.code}"
                )

            voltagetype = self.voltagetype.getbyname(name=item.name)
            if voltagetype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Voltage Type already registered with name {item.name}"
                )
            
            voltagetype = self.voltagetype.getbyshortname(shortname=item.shortname)
            if voltagetype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Voltage Type already registered with shortname {item.name}"
                )
        return self.voltagetype.create(data=data)

    # update voltage type function
    async def update(self, code: int, data: VoltageTypeUpdate) -> VoltageTypeUpdate:
        old_data = jsonable_encoder(self.voltagetype.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Voltage Type not found"
            )
        
        current_data = jsonable_encoder(self.voltagetype.update(code=code, data=data.dict()))
        logs = [await build_log(f"/voltagetypes/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        await self.log.create(logs)
        return current_data
    
    # delete voltage type function
    async def delete(self, code: int) -> None:
        data = self.voltagetype.getbycode(code=code)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Voltage Type not found",
            )

        self.voltagetype.delete(data)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Voltage Type deleted",
        )