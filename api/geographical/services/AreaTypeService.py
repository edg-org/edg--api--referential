from typing import List
from fastapi import Depends, HTTPException, status
from api.geographical.models.AreaTypeModel import AreaTypeModel
from api.geographical.repositories.AreaTypeRepo import AreaTypeRepo
from api.geographical.schemas.AreaTypeSchema import AreaTypeBase, CreateAreaType

class AreaTypeService:
    areatype: AreaTypeRepo

    def __init__(
        self, areatype: AreaTypeRepo = Depends()
    ) -> None:
        self.areatype = areatype

    # get all area types function
    async def list(self, skip: int = 0, limit: int = 100) -> List[AreaTypeModel]:
        return self.areatype.list(skip=skip, limit=limit)

    # get area type by id function
    async def get(self, id: int) -> AreaTypeModel:
        return self.areatype.get(id=id)
    
    # get area type by code function
    async def getbycode(self, code: str) -> AreaTypeBase:
        return self.areatype.getbycode(code=code)
    
    # get area type by name function
    async def getbyname(self, name: str) -> AreaTypeBase:
        return self.areatype.getbyname(name=name)

    # create area type function
    async def create(self, data: List[CreateAreaType]) -> List[CreateAreaType]:
        for item in data:
            areatype = self.areatype.getbycode(code=item.code)
            if areatype:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Area Type already registered with code "+ str(item.code))
            
            areatype = self.areatype.getbyname(name=item.name)
            if areatype:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Area Type already registered with name "+ item.name)
        
        return self.areatype.create(data=data)

    # update area type function
    async def update(self, code: int, data: AreaTypeBase) -> AreaTypeModel:
        areatype = self.areatype.get(code=code)
        if areatype is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area Type not found")
        
        typedict = data.dict(exclude_unset=True)
        for key, val in typedict.items():
            setattr(areatype, key, val)
        return self.areatype.update(areatype)

    # delete area type %function
    async def delete(self, area: AreaTypeModel) -> None:
        areatype = self.areatype.get(id=id)
        if areatype is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area Type not found")
        
        self.areatype.update(area)
        return HTTPException(status_code=status.HTTP_200_OK, detail="Area Type deleted")