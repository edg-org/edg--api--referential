from typing import List
from fastapi import Depends, HTTPException, status
from api.electrical.models.VoltageTypeModel import VoltageTypeModel
from api.electrical.repositories.VoltageTypeRepo import VoltageTypeRepo
from api.electrical.schemas.VoltageTypeSchema import (
    VoltageTypeBase,
    VoltageTypeUpdate,
    CreateVoltageType
)

#
class VoltageTypeService:
    voltagetype: VoltageTypeRepo

    def __init__(
        self, voltagetype: VoltageTypeRepo = Depends()
    ) -> None:
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
    async def getbycode(self, code: str) -> VoltageTypeBase:
        return self.voltagetype.getbycode(code=code)

    # get voltage type by name function
    async def getbyname(self, name: str) -> VoltageTypeBase:
        return self.voltagetype.getbyname(name=name)

    # create voltage type function
    async def create(self, data: List[CreateVoltageType]) -> List[CreateVoltageType]:
        for item in data:
            voltagetype = self.voltagetype.getbycode(code=item.code)
            if voltagetype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Voltage Type already registered with code " + str(item.code),
                )

            voltagetype = self.voltagetype.getbyname(name=item.name)
            if voltagetype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Voltage Type already registered with name " + item.name,
                )
            
            voltagetype = self.voltagetype.getbyshortname(shortname=item.shortname)
            if voltagetype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Voltage Type already registered with shortname " + item.name,
                )
        return self.voltagetype.create(data=data)

    # update voltage type function
    async def update(self, code: int, data: VoltageTypeUpdate) -> VoltageTypeUpdate:
        voltagetype = self.voltagetype.getbycode(code=code)
        if voltagetype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Voltage Type not found",
            )

        voltagetypedict = data.dict(exclude_unset=True)
        for key, val in voltagetypedict.items():
            setattr(voltagetype, key, val)
        return self.voltagetype.update(voltagetype)

    # delete voltage type function
    async def delete(self, type: VoltageTypeModel) -> None:
        voltagetype = self.voltagetype.get(id=id)
        if voltagetype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Voltage Type not found",
            )

        self.voltagetype.update(type)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Voltage Type deleted",
        )