from typing import List
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from api.logs.repositories.LogRepo import LogRepo
from fastapi import Depends, HTTPException, status
from api.ageographical.models.AreaTypeModel import AreaTypeModel
from api.ageographical.schemas.AreaTypeSchema import CreateAreaType
from api.ageographical.repositories.AreaTypeRepo import AreaTypeRepo

#
class AreaTypeService:
    log: LogRepo
    areatype: AreaTypeRepo

    def __init__(
        self, 
        log: LogRepo = Depends(),
        areatype: AreaTypeRepo = Depends()
    ) -> None:
        self.log = log
        self.areatype = areatype

    # get all area types function
    async def list(self, skip: int = 0, limit: int = 100) -> List[AreaTypeModel]:
        return self.areatype.list(skip=skip, limit=limit)

    # get area type by id function
    async def get(self, id: int) -> AreaTypeModel:
        return self.areatype.get(id=id)

    # get area type by code function
    async def getbycode(self, code: str) -> AreaTypeModel:
        return self.areatype.getbycode(code=code)

    # get area type by name function
    async def getbyname(self, name: str) -> AreaTypeModel:
        return self.areatype.getbyname(name=name)

    # create area type function
    async def create(self, data: List[CreateAreaType]) -> List[CreateAreaType]:
        for item in data:
            areatype = self.areatype.getbycode(code=item.code)
            if areatype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Area Type already registered with code {item.code}"
                )

            areatype = self.areatype.getbyname(name=item.name)
            if areatype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Area Type already registered with name {item.name}"
                )

        return self.areatype.create(data=data)

    # update area type function
    async def update(self, code: int, tokendata: dict, data: CreateAreaType) -> AreaTypeModel:
        old_data = jsonable_encoder(self.areatype.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Area Type not found"
            )

        current_data = jsonable_encoder(self.areatype.update(code=code, data=data.dict()))
        logs = [await Helper.build_log(f"/areatypes/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # delete area type %function
    async def delete(self, code: int) -> None:
        data = self.areatype.getbycode(code=code)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Area Type not found",
            )

        self.areatype.delete(data)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Area Type deleted",
        )