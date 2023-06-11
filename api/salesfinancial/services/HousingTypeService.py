from typing import List
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from api.logs.services.LogService import LogService
from api.salesfinancial.models.HousingTypeModel import HousingTypeModel
from api.salesfinancial.repositories.HousingTypeRepo import HousingTypeRepo
from api.salesfinancial.schemas.HousingTypeSchema import CreateHousingType, HousingTypeUpdate

class HousingTypeService:
    log: LogService
    housingtype: HousingTypeRepo

    def __init__(
        self, 
        log: LogService = Depends(),
        housingtype: HousingTypeRepo = Depends()
    ) -> None:
        self.log = log
        self.housingtype = housingtype

    # get all housing types function
    async def list(self, skip: int = 0, limit: int = 100) -> List[HousingTypeModel]:
        return self.housingtype.list(skip=skip, limit=limit)

    # get housing type by id function
    async def get(self, id: int) -> HousingTypeModel:
        return self.housingtype.get(id=id)

    # get housing type by code function
    async def getbycode(self, code: str) -> HousingTypeModel:
        return self.housingtype.getbycode(code=code)

    # get housing type by name function
    async def getbyname(self, name: str) -> HousingTypeModel:
        return self.housingtype.getbyname(name=name)

    # create housing type function
    async def create(self, data: List[CreateHousingType]) -> List[CreateHousingType]:
        for item in data:
            housingtype = self.housingtype.getbycode(code=item.code)
            if housingtype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Housing Type already registered with code {item.code}",
                )

            housingtype = self.housingtype.getbyname(name=item.name)
            if housingtype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Housing Type already registered with name {item.name}",
                )

        return self.housingtype.create(data=data)

    # update housing type function
    async def update(self, code: int, tokendata: dict, data: HousingTypeUpdate) -> HousingTypeModel:
        old_data = jsonable_encoder(self.housingtype.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Housing Type not found",
            )
        
        current_data = jsonable_encoder(self.housingtype.update(code, data=data.dict()))
        logs = [await Helper.build_log(f"/housingtypes/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # delete housing type %function
    async def delete(self, code: int) -> None:
        data = self.housingtype.getbycode(code=code)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Housing Type not found",
            )

        self.housingtype.delete(data)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Housing Type deleted",
        )