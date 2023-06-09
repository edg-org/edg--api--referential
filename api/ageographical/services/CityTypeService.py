from typing import List
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from api.logs.services.LogService import LogService
from api.ageographical.models.CityTypeModel import CityTypeModel
from api.ageographical.repositories.CityTypeRepo import CityTypeRepo
from api.ageographical.schemas.CityTypeSchema import CreateCityType

#
class CityTypeService:
    log: LogService
    citytype: CityTypeRepo

    def __init__(
        self, 
        log: LogService = Depends(),
        citytype: CityTypeRepo = Depends()
    ) -> None:
        self.log = log
        self.citytype = citytype

    # get all city types function
    async def list(self, start: int = 0, size: int = 100) -> List[CityTypeModel]:
        return self.citytype.list(start=start, size=size)

    # get city type by id function
    async def get(self, id: int) -> CityTypeModel:
        return self.citytype.get(id=id)

    # get city type by code function
    async def getbycode(self, code: str) -> CityTypeModel:
        return self.citytype.getbycode(code=code)

    # get city type by name function
    async def getbyname(self, name: str) -> CityTypeModel:
        return self.citytype.getbyname(name=name)

    # create city type function
    async def create(self, data: List[CreateCityType]) -> List[CreateCityType]:
        for item in data:
            citytype = self.citytype.getbycode(code=item.code)
            if citytype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"City Type already registered with code {item.code}",
                )

            citytype = self.citytype.getbyname(name=item.name)
            if citytype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"City Type already registered with name {item.name}",
                )

        return self.citytype.create(data=data)

    # update city type function
    async def update(self, code: int, tokendata: dict, data: CreateCityType) -> CityTypeModel:
        old_data = jsonable_encoder(self.citytype.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City Type not found",
            )

        current_data = jsonable_encoder(self.citytype.update(code, data=data.dict()))
        logs = [await Helper.build_log(f"/citytypes/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return current_data

   # delete city type function
    async def delete(self, code: int) -> None:
        data = self.areatype.getbycode(code=code)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City Type not found",
            )

        self.areatype.delete(data)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="City Type deleted",
        )