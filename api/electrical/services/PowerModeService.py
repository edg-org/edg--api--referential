from typing import List
from fastapi import Depends, HTTPException, status
from api.electrical.models.PowerModeModel import (
    PowerModeModel,
)
from api.electrical.repositories.PowerModeRepo import (
    PowerModeRepo,
)
from api.electrical.schemas.PowerModeSchema import (
    PowerModeBase,
    CreatePowerMode,
)


#
class PowerModeService:
    powermode: PowerModeRepo

    def __init__(
        self, powermode: PowerModeRepo = Depends()
    ) -> None:
        self.powermode = powermode

    # get all power modes function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[PowerModeModel]:
        return self.powermode.list(skip=skip, limit=limit)

    # get power mode by id function
    async def get(self, id: int) -> PowerModeModel:
        return self.powermode.get(id=id)

    # get power mode by code function
    async def getbycode(self, code: str) -> PowerModeBase:
        return self.powermode.getbycode(code=code)

    # get power mode by name function
    async def getbyname(self, name: str) -> PowerModeBase:
        return self.powermode.getbyname(name=name)

    # create power mode function
    async def create(
        self, data: List[CreatePowerMode]
    ) -> List[CreatePowerMode]:
        for item in data:
            powermode = self.powermode.getbycode(
                code=item.code
            )
            if powermode:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Power Mode already registered with code "
                    + str(item.code),
                )

            powermode = self.powermode.getbyname(
                name=item.name
            )
            if powermode:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Power Mode already registered with name "
                    + item.name,
                )

        return self.powermode.create(data=data)

    # update power mode function
    async def update(
        self, code: int, data: PowerModeBase
    ) -> PowerModeModel:
        powermode = self.powermode.getbycode(code=code)
        if powermode is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Power Mode not found",
            )

        modedict = data.dict(exclude_unset=True)
        for key, val in modedict.items():
            setattr(powermode, key, val)
        return self.powermode.update(powermode)

    # delete power mode function
    async def delete(self, mode: PowerModeModel) -> None:
        powermode = self.powermode.get(id=id)
        if powermode is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Power Mode not found",
            )

        self.powermode.update(mode)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Power Mode deleted",
        )
