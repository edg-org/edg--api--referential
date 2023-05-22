from typing import List
from fastapi import Depends, HTTPException, status
from api.salesfinancial.models.HousingTypeModel import HousingTypeModel
from api.salesfinancial.schemas.HousingTypeSchema import CreateHousingType
from api.salesfinancial.repositories.HousingTypeRepo import HousingTypeRepo

class HousingTypeService:
    housingtype: HousingTypeRepo

    def __init__(
        self, housingtype: HousingTypeRepo = Depends()
    ) -> None:
        self.housingtype = housingtype

    # get all housing types function
    async def list(self, skip: int = 0, limit: int = 100) -> List[HousingTypeModel]:
        return self.housingtype.list(
            skip=skip, limit=limit
        )

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
                    detail="Housing Type already registered with code "
                    + str(item.code),
                )

            housingtype = self.housingtype.getbyname(name=item.name)
            if housingtype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Housing Type already registered with name "
                    + item.name,
                )

        return self.housingtype.create(data=data)

    # update housing type function
    async def update(self, code: int, data: CreateHousingType) -> HousingTypeModel:
        housingtype = self.housingtype.getbycode(code=code)
        if housingtype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Housing Type not found",
            )

        typedict = data.dict(exclude_unset=True)
        for key, val in typedict.items():
            setattr(housingtype, key, val)
        return self.housingtype.update(housingtype)

    # delete housing type %function
    async def delete(self, housing: HousingTypeModel) -> None:
        housingtype = self.housingtype.getbycode(code=code)
        if housingtype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Housing Type not found",
            )

        self.housingtype.update(housing)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Housing Type deleted",
        )
