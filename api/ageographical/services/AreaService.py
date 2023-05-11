from typing import List
from fastapi import Depends, HTTPException, status
from api.ageographical.models.AreaModel import AreaModel
from api.ageographical.repositories.AreaRepo import AreaRepo
from api.ageographical.repositories.CityRepo import CityRepo
from api.ageographical.repositories.AgencyRepo import AgencyRepo
from api.ageographical.repositories.AreaTypeRepo import AreaTypeRepo
from api.tools.Helper import area_basecode, generate_zipcode, generate_code
from api.ageographical.schemas.AreaSchema import (
    AreaInput,
    AreaUpdate,
    CreateArea,
)


class AreaService:
    area: AreaRepo

    def __init__(self, area: AreaRepo = Depends()) -> None:
        self.area = area

    # get all areas function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[AreaModel]:
        return self.area.list(skip=skip, limit=limit)

    # get area by id function
    async def get(self, id: int) -> AreaModel:
        return self.area.get(id=id)

    # get area by code function
    async def getbycode(self, code: str) -> AreaModel:
        return self.area.getbycode(code=code)

    # get area by name function
    async def getbyname(self, name: str) -> AreaModel:
        return self.area.getbyname(name=name)

    # create area function
    async def create(self, data: List[AreaInput]) -> List[CreateArea]:
        step = 0
        arealist = []
        place_code = 0
        step_zipcode = 0
        for item in data:
            step +=1
            input_code = 0
            maxcode=0
            hierarchical_area_id = None
            city_id = 0
            zipcode = 0
            if (hasattr(item.infos, "hierarchical_area_code") and item.infos.hierarchical_area_code is not None):
                count = self.area.checknamebyhierarchicalareacode(hierarchical_area_code=item.infos.hierarchical_area_code, name=item.infos.name)
                if count > 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Area already registered with name " + item.infos.name + " whose hierarchical area code is " + str(item.infos.hierarchical_area_code),
                    )
                    
                area = AreaRepo.getbycode(self.area, item.infos.hierarchical_area_code)
                city_id = area.city_id
                zipcode = area.zipcode
                hierarchical_area_id =  area.id
                input_code = item.infos.hierarchical_area_code
                maxcode=self.area.maxcodebyhierachicalarea(input_code)
            elif (hasattr(item.infos, "city_code") and item.infos.city_code is not None):
                count = self.area.checknamebycitycode(hierarchical_area_code=item.infos.city_code, name=item.infos.name)
                if count > 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Area already registered with name " + item.infos.name + " in the city whose code is " + str(item.infos.city_code),
                    )
                input_code = item.infos.city_code
                maxcode=self.area.maxcodebycity(input_code)
                city_id = CityRepo.getidbycode(self.area, item.infos.city_code)
                zipcode = CityRepo.getbycode(self.area, item.infos.city_code).zipcode
                
            result = generate_code(
                init_codebase=area_basecode(input_code),
                maxcode=maxcode,
                input_code=input_code,
                code=place_code,
                step=step,
                init_step=1
            )
            
            step = result["step"]
            area_code = result["code"]
            count = self.area.countbycode(code=area_code)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Area already registered with code " + str(area_code)
                )
                
            if item.infos.on_hierarchical_zipcode == False:
                step_zipcode +=1
                zipcode = generate_zipcode(int(zipcode), step_zipcode)

            agency_id = None
            if (hasattr(item.infos, "agency_code") and item.infos.agency_code is not None):
                agency_id = AgencyRepo.getidbycode(self.area, item.infos.agency_code)

            area = CreateArea(
                code = area_code,
                zipcode = zipcode,
                agency_id = agency_id,
                hierarchical_area_id = hierarchical_area_id,
                city_id = city_id,
                area_type_id = AreaTypeRepo.getbyname(self.area, item.infos.area_type).id,
                infos = item.infos
            )
            
            print(area)
            arealist.append(area)
            place_code = item.infos.city_code
            if (hasattr(item.infos, "hierarchical_area_code") and item.infos.hierarchical_area_code is not None):
                place_code = item.infos.hierarchical_area_code

        return "dededeededed"#self.area.create(data=arealist)

    # update area function
    async def update(self, code: int, data: AreaUpdate) -> AreaModel:
        count = self.area.countbycode(code=code)
        if count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Area not found",
            )
        
        olddata = self.area.getbycode(code=code)
        agency_id = olddata.agency_id
        if (hasattr(data.infos, "agency_code") and data.infos.agency_code is not None):
            agency_id = AgencyRepo.getidbycode(self.area, data.infos.agency_code)

        area = CreateArea(
            code = code,
            zipcode = olddata.zipcode,
            city_id = CityRepo.getidbycode(self.area, data.infos.city_code),
            agency_id = agency_id,
            area_type_id = AreaTypeRepo.getbyname(self.area, data.infos.area_type).id,
            infos = item.infos
        )

        areadict = data.dict(exclude_unset=True)
        for key, val in areadict.items():
            setattr(area, key, val)
        return self.area.update(area)

    # delete area function
    async def delete(self, area: AreaModel) -> None:
        area = self.area.getbycode(code=code)
        if area is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Area not found",
            )

        self.area.update(area)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Area deleted",
        )