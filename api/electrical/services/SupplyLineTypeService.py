from typing import List
from fastapi import Depends, HTTPException, status
from api.electrical.models.SupplyLineTypeModel import SupplyLineTypeModel
from api.electrical.repositories.SupplyLineTypeRepo import SupplyLineTypeRepo
from api.electrical.schemas.SupplyLineTypeSchema import (
    SupplyLineTypeBase,
    SupplyLineTypeUpdate,
    CreateSupplyLineType
)

#
class SupplyLineTypeService:
    supplytype: SupplyLineTypeRepo

    def __init__(
        self, supplytype: SupplyLineTypeRepo = Depends()
    ) -> None:
        self.supplytype = supplytype

    # get all supply line types function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[SupplyLineTypeModel]:
        return self.supplytype.list(skip=skip, limit=limit)

    # get supply line type by id function
    async def get(self, id: int) -> SupplyLineTypeModel:
        return self.supplytype.get(id=id)

    # get supply line type by code function
    async def getbycode(self, code: str) -> SupplyLineTypeBase:
        return self.supplytype.getbycode(code=code)

    # get supply line type by name function
    async def getbyname(self, name: str) -> SupplyLineTypeBase:
        return self.supplytype.getbyname(name=name)

    # create supply line type function
    async def create(self, data: List[CreateSupplyLineType]) -> List[CreateSupplyLineType]:
        for item in data:
            supplytype = self.supplytype.getbycode(code=item.code)
            if supplytype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Supply Line Type already registered with code " + str(item.code),
                )

            supplytype = self.supplytype.getbyname(name=item.name)
            if supplytype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Supply Line Type already registered with name " + item.name,
                )
        return self.supplytype.create(data=data)

    # update supply line type function
    async def update(self, code: int, data: SupplyLineTypeUpdate) -> SupplyLineTypeUpdate:
        supplytype = self.supplytype.getbycode(code=code)
        if supplytype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supply Line Type not found",
            )

        typedict = data.dict(exclude_unset=True)
        for key, val in typedict.items():
            setattr(supplytype, key, val)
        return self.supplytype.update(supplytype)

    # delete supply line type function
    async def delete(self, type: SupplyLineTypeModel) -> None:
        supplytype = self.supplytype.get(id=id)
        if supplytype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supply Line Type not found",
            )

        self.supplytype.update(type)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Supply Line Type deleted",
        )