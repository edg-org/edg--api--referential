from typing import List
from api.tools.Helper import build_log
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from api.logs.services.LogService import LogService
from api.ageographical.models.CityTypeModel import CityTypeModel
from api.ageographical.repositories.CityTypeRepo import CityTypeRepo
from api.ageographical.schemas.CityTypeSchema import CreateCityType
from api.logs.repositories.LogRepo import LogRepo
#
class CityTypeService:
    log: LogRepo
    citytype: CityTypeRepo

    def __init__(self, citytype: CityTypeRepo = Depends(), log: LogRepo = Depends()) -> None:
        self.log = log
        self.citytype = citytype

    # get all city types function
    async def list(self, skip: int = 0, limit: int = 100) -> List[CityTypeModel]:
        return self.citytype.list(skip=skip, limit=limit)

    # get city type by id function
    async def get(self, id: int) -> CityTypeModel:
        return self.citytype.get(id=id)

    # get city type by code function
    async def getbycode(self, code: int) -> CityTypeModel:
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
    async def update(self, code: int, data: CreateCityType) -> CityTypeModel:
        old_data = jsonable_encoder(self.citytype.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City Type not found",
            )

        current_data = jsonable_encoder(self.citytype.update(code, data=data.dict()))
        logs = [await build_log(f"/citytypes/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        self.log.create(logs)
        return current_data

    # delete city type function
    async def delete(self, code: int) -> None:
        data = self.citytype.getbycode(code=code)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City Type not found",
            )

        self.citytype.delete(data)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="City Type deleted",
        )
