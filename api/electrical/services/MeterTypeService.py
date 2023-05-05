from typing import List
from fastapi import Depends, HTTPException, status
from api.electrical.models.MeterTypeModel import MeterTypeModel
from api.electrical.repositories.MeterTypeRepo import MeterTypeRepo
from api.electrical.schemas.MeterTypeSchema import (
    MeterTypeBase,
    CreateMeterType,
)


#
class MeterTypeService:
    metertype: MeterTypeRepo

    def __init__(
        self, metertype: MeterTypeRepo = Depends()
    ) -> None:
        self.metertype = metertype

    # get all meter types function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[MeterTypeModel]:
        return self.metertype.list(skip=skip, limit=limit)

    # get meter type by id function
    async def get(self, id: int) -> MeterTypeModel:
        return self.metertype.get(id=id)

    # get meter type by code function
    async def getbycode(self, code: str) -> MeterTypeBase:
        return self.metertype.getbycode(code=code)

    # get meter type by name function
    async def getbyname(self, name: str) -> MeterTypeBase:
        return self.metertype.getbyname(name=name)

    # create meter type function
    async def create(
        self, data: List[CreateMeterType]
    ) -> List[CreateMeterType]:
        for item in data:
            metertype = self.metertype.getbycode(
                code=item.code
            )
            if metertype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Meter Type already registered with code "
                    + str(item.code),
                )

            metertype = self.metertype.getbyname(
                name=item.name
            )
            if metertype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Meter Type already registered with name "
                    + item.name,
                )

        return self.metertype.create(data=data)

    # update meter type function
    async def update(
        self, code: int, data: MeterTypeBase
    ) -> MeterTypeModel:
        metertype = self.metertype.getbycode(code=code)
        if metertype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meter Type not found",
            )

        typedict = data.dict(exclude_unset=True)
        for key, val in typedict.items():
            setattr(metertype, key, val)
        return self.metertype.update(metertype)

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
