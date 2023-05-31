from typing import List
from fastapi import Depends, HTTPException, status
from api.ageographical.models.CityTypeModel import CityTypeModel
from api.ageographical.repositories.CityTypeRepo import CityTypeRepo
from api.ageographical.schemas.CityTypeSchema import CreateCityType

#
class CityTypeService:
    citytype: CityTypeRepo

    def __init__(
        self, citytype: CityTypeRepo = Depends()
    ) -> None:
        self.citytype = citytype

    # get all city types function
    async def list(self, skip: int = 0, limit: int = 100) -> List[CityTypeModel]:
        return self.citytype.list(skip=skip, limit=limit)

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
                    detail="City Type already registered with code "
                    + str(item.code),
                )

            citytype = self.citytype.getbyname(name=item.name)
            if citytype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="City Type already registered with name "
                    + item.name,
                )

        return self.citytype.create(data=data)

    # update city type function
    async def update(self, code: int, data: CreateCityType) -> CityTypeModel:
        citytype = self.citytype.getbycode(code=code)
        if citytype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City Type not found",
            )

        citydict = data.dict(exclude_unset=True)
        for key, val in citydict.items():
            setattr(citytype, key, val)
        return self.citytype.update(citytype)

    # delete city type function
    async def delete(self, city: CityTypeModel) -> None:
        citytype = self.citytype.getbycode(code=code)
        if citytype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City Type not found",
            )

        self.citytype.update(city)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="City Type deleted",
        )
