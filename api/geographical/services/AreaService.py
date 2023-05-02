from typing import List
from api.tools.Helper import area_basecode
from fastapi import Depends, HTTPException, status
from api.geographical.models.AreaModel import AreaModel
from api.geographical.repositories.AreaRepo import AreaRepo
from api.geographical.repositories.CityRepo import CityRepo
from api.geographical.schemas.AreaSchema import AreaBase, CreateArea

class AreaService:
    area: AreaRepo

    def __init__(
        self, area: AreaRepo = Depends()
    ) -> None:
        self.area = area

    # get all areas function
    async def list(self, skip: int = 0, limit: int = 100) -> List[AreaModel]:
        return self.area.list(skip=skip, limit=limit)

    # get area by id function
    async def get(self, id: int) -> AreaModel:
        return self.area.get(id=id)
    
    # get area by code function
    async def getbycode(self, code: str) -> AreaBase:
        return self.area.getbycode(code=code)
    
    # get area by name function
    async def getbyname(self, name: str) -> AreaBase:
        return self.area.getbyname(name=name)

    # create area function
    async def create(self, data: List[CreateArea]) -> List[CreateArea]:
        city_code = 0
        for item in data:
            maxcode = self.area.maxcode_bycity(item.infos.city_code)
            if maxcode is None:
                maxcode = 0
            
            item.city_id = CityRepo.getid_bycode(self.area, item.infos.city_code)

            if maxcode > 0:
                step +=1
                basecode = maxcode
            else:
                basecode = area_basecode(item.infos.city_code)
                if city_code == item.infos.city_code:
                    step +=1
                else:
                    step = 0
            
            area_code = basecode+step
            city_code = item.infos.city_code
            item.code = area_code
            area = self.area.getbycode(code=item.code)
            if area:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Area already registered with code "+ str(item.code))
            
            area = self.area.getbyname(name=item.infos.name)
            if area:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Area already registered with name "+ item.infos.name)
        
        return self.area.create(data=data)

    # update area function
    async def update(self, code: int, data: AreaBase) -> AreaModel:
        area = self.area.getbycode(code=code)
        if area is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
        
        areadict = data.dict(exclude_unset=True)
        for key, val in areadict.items():
            setattr(area, key, val)
        return self.area.update(area)

    # delete area function
    async def delete(self, area: AreaModel) -> None:
        area = self.area.get(id=id)
        if area is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
        
        self.area.update(area)
        return HTTPException(status_code=status.HTTP_200_OK, detail="Area deleted")