from typing import List
from api.tools.Helper import build_log
from fastapi.encoders import jsonable_encoder
from api.logs.repositories.LogRepo import LogRepo
from fastapi import Depends, HTTPException, status
from api.electrical.models.SupplyModeModel import SupplyModeModel
from api.electrical.schemas.SupplyModeSchema import CreateSupplyMode
from api.electrical.repositories.SupplyModeRepo import SupplyModeRepo

class SupplyModeService:
    log: LogRepo
    supplymode: SupplyModeRepo

    def __init__(
        self, 
        log: LogRepo = Depends(),
        supplymode: SupplyModeRepo = Depends()
    ) -> None:
        self.log = log
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
    async def create(self, data: List[CreateSupplyMode]) -> List[CreateSupplyMode]:
        for item in data:
            supplymode = self.supplymode.getbycode(code=item.code)
            if supplymode:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Supply Mode already registered with code {item.code}",
                )

            supplymode = self.supplymode.getbyname(name=item.name)
            if supplymode:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Supply Mode already registered with name {item.name}",
                )

        return self.supplymode.create(data=data)

    # update supply mode function
    async def update(self, code: int, data: SupplyModeModel) -> SupplyModeModel:
        old_data = jsonable_encoder(self.supplymode.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supply Mode not found"
            )
    
        current_data = jsonable_encoder(self.supplymode.update(code=code, data=data.dict()))
        logs = [await build_log(f"/supplymodes/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        self.log.create(logs)
        return current_data

    # delete supply mode function
    async def delete(self, code: int) -> None:
        data = self.supplymode.getbycode(code=code)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supply Mode not found"
            )

        self.supplymode.delete(data)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Supply Mode deleted"
        )
