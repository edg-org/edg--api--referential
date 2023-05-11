from typing import List
from fastapi import Depends, HTTPException, status
from api.ageographical.models.AreaModel import AreaModel
from api.tools.Helper import area_basecode, generate_zipcode
from api.ageographical.repositories.AreaRepo import AreaRepo
from api.ageographical.repositories.CityRepo import CityRepo
from api.ageographical.repositories.AgencyRepo import AgencyRepo
from api.ageographical.repositories.AreaTypeRepo import AreaTypeRepo
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
        city_code = 0
        step_zipcode = 0
        for item in data:
            count = self.area.countbyname(name=item.infos.name)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Area already registered with name " + item.infos.name
                )

            step +=1
            result = generate_code(
                init_codebase=area_basecode(item.infos.city_code),
                maxcode=self.area.maxcodebycity(item.infos.city_code),
                input_code=item.infos.city_code,
                code=city_code,
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

            zipcode = CityRepo.getbycode(self.area, item.infos.city_code).zipcode
            if item.infos.on_city_zipcode == False:
                step_zipcode +=1
                zipcode = generate_zipcode(int(zipcode), step_zipcode)

            agency_id = None
            if (hasattr(item.infos, "agency_code") and item.infos.agency_code is not None):
                agency_id = AgencyRepo.getidbycode(self.area, item.infos.agency_code)

            area = CreateArea(
                code = area_code,
                zipcode = zipcode,
                city_id = CityRepo.getidbycode(self.area, item.infos.city_code),
                agency_id = agency_id,
                area_type_id = AreaTypeRepo.getbyname(self.area, item.infos.area_type).id,
                infos = item.infos
            )

            arealist.append(area)
            city_code = item.infos.city_code

        return self.area.create(data=arealist)

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
