from typing import List
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from api.logs.repositories.LogRepo import LogRepo
from fastapi import Depends, HTTPException, status
from api.ageographical.models.CityLevelModel import CityLevelModel
from api.ageographical.schemas.CityLevelSchema import CreateCityLevel
from api.ageographical.repositories.CityLevelRepo import CityLevelRepo

#
class CityLevelService:
    log: LogRepo
    citylevel: CityLevelRepo

    def __init__(
        self, 
        log: LogRepo = Depends(),
        citylevel: CityLevelRepo = Depends()
    ) -> None:
        self.log = log
        self.citylevel = citylevel

    # get all city levels function
    async def list(self, skip: int = 0, limit: int = 100) -> List[CityLevelModel]:
        return self.citylevel.list(skip=skip, limit=limit)

    # get city level by id function
    async def get(self, id: int) -> CityLevelModel:
        return self.citylevel.get(id=id)

    # get city level by code function
    async def getbycode(self, code: str) -> CityLevelModel:
        return self.citylevel.getbycode(code=code)

    # get city level by name function
    async def getbyname(self, name: str) -> CityLevelModel:
        return self.citylevel.getbyname(name=name)

    # create city level function
    async def create(self, data: List[CreateCityLevel]) -> List[CreateCityLevel]:
        for item in data:
            citylevel = self.citylevel.getbycode(code=item.code)
            if citylevel:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"City Level already registered with code {item.code}",
                )

            citylevel = self.citylevel.getbyname(name=item.name)
            if citylevel:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"City Level already registered with name {item.name}",
                )

        return self.citylevel.create(data=data)

    # update city level function
    async def update(self, code: int, tokendata: dict, data: CreateCityLevel) -> CityLevelModel:
        old_data = jsonable_encoder(self.citylevel.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City Level not found",
            )

        current_data = jsonable_encoder(self.citytype.update(code=code, data=data.dict()))
        logs = [await Helper.build_log(f"/citylevels/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # delete city level %function
    async def delete(self, code: int) -> None:
        data = self.citylevel.getbycode(code=code)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City Level not found",
            )

        self.citylevel.delete(data)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="City Level deleted",
        )