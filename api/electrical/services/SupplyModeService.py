from typing import List
from fastapi import Depends, HTTPException, status
from api.electrical.models.SupplyModeModel import SupplyModeModel
from api.electrical.repositories.SupplyModeRepo import SupplyModeRepo
from api.electrical.schemas.SupplyModeSchema import CreateSupplyMode

#
class SupplyModeService:
    supplymode: SupplyModeRepo

    def __init__(
        self, supplymode: SupplyModeRepo = Depends()
    ) -> None:
        self.supplymode = supplymode

    # get all supply modes function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[SupplyModeModel]:
        return self.supplymode.list(skip=skip, limit=limit)

    # get supply mode by id function
    async def get(self, id: int) -> SupplyModeModel:
        return self.supplymode.get(id=id)

    # get supply mode by code function
    async def getbycode(self, code: str) -> SupplyModeModel:
        return self.supplymode.getbycode(code=code)

    # get supply mode by name function
    async def getbyname(self, name: str) -> SupplyModeModel:
        return self.supplymode.getbyname(name=name)

    # create supply mode function
    async def create(
        self, data: List[CreateSupplyMode]
    ) -> List[CreateSupplyMode]:
        for item in data:
            supplymode = self.supplymode.getbycode(code=item.code)
            if supplymode:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Supply Mode already registered with code "
                    + str(item.code),
                )

            supplymode = self.supplymode.getbyname(name=item.name)
            if supplymode:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Supply Mode already registered with name "
                    + item.name,
                )

        return self.supplymode.create(data=data)

    # update supply mode function
    async def update(
        self, code: int, data: SupplyModeModel
    ) -> SupplyModeModel:
        supplymode = self.supplymode.getbycode(code=code)
        if supplymode is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supply Mode not found",
            )

        modedict = data.dict(exclude_unset=True)
        for key, val in modedict.items():
            setattr(supplymode, key, val)
        return self.supplymode.update(supplymode)

    # delete supply mode function
    async def delete(self, mode: SupplyModeModel) -> None:
        supplymode = self.supplymode.get(id=id)
        if supplymode is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supply Mode not found",
            )

        self.supplymode.update(mode)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Supply Mode deleted",
        )
