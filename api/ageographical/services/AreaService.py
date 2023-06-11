from typing import List
from datetime import datetime
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from api.logs.repositories.LogRepo import LogRepo
from fastapi import Depends, HTTPException, status
from api.ageographical.models.AreaModel import AreaModel
from api.ageographical.repositories.AreaRepo import AreaRepo
from api.ageographical.repositories.CityRepo import CityRepo
from api.ageographical.repositories.AgencyRepo import AgencyRepo
from api.ageographical.repositories.AreaTypeRepo import AreaTypeRepo
from api.ageographical.schemas.AreaSchema import (
    AreaInput,
    AreaUpdate,
    CreateArea
)

#
class AreaService:
    log: LogRepo
    area: AreaRepo

    def __init__(
        self, 
        log: LogRepo = Depends(),
        area: AreaRepo = Depends()
    ) -> None:
        self.log = log
        self.area = area

    # get all areas function
    async def list(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[AreaModel]:
        return self.area.list(skip=skip, limit=limit)

    # get area by id function
    async def get(self, id: int) -> AreaModel:
        return self.area.get(id=id)

    # get area by code function
    async def getbycode(self, code: int) -> AreaModel:
        return self.area.getbycode(code=code)

    # get area by name function
    async def getbyname(self, name: str) -> AreaModel:
        return self.area.getbyname(name=name)

    # create area function
    async def create(self, data: List[AreaInput]) -> List[CreateArea]:
        step = 0
        arealist = []
        area_type = None
        place_code = None
        step_zipcode = 0
        no_hirearchical_type = AreaTypeRepo.no_hierarchical_type(self.area)
    
        for item in data:
            maxcode = 0
            city_id = 0
            zipcode = 0
            input_code = 0
            area_type_id = 0
            hierarchical_area_id = None
            
            if (
                hasattr(item.infos, "hierarchical_area_code") 
                and item.infos.hierarchical_area_code is not None
                and str(item.infos.area_type).lower() not in no_hirearchical_type
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"The area type must be in {no_hirearchical_type}"
                )
                
            if (
                hasattr(item.infos, "hierarchical_area_code") 
                and item.infos.hierarchical_area_code is not None
                and str(item.infos.area_type).lower() in no_hirearchical_type
            ):
                count = self.area.checkname_by_hierarchy(
                    hierarchical_area_code=item.infos.hierarchical_area_code, 
                    name=item.infos.name
                )
                if count > 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Area already registered with name {item.infos.name} whose hierarchical area code is {item.infos.hierarchical_area_code}"
                    )
                area = AreaRepo.getbycode(self.area, item.infos.hierarchical_area_code)
                city_id = area.city_id
                zipcode = area.zipcode
                hierarchical_area_id =  area.id
                input_code = item.infos.hierarchical_area_code
                maxcode = self.area.maxcode_by_areaandtype(input_code, area_type_id)
                item.infos.city_code = CityRepo.get(self.area, area.city_id).code
                area_type_id = AreaTypeRepo.getbyname(self.area, item.infos.area_type).id
            
            elif (hasattr(item.infos, "city_code") and item.infos.city_code is not None):
                count = self.area.checkname_by_citycode(
                    city_code=item.infos.city_code, 
                    name=item.infos.name
                )
                if count > 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Area already registered with name {item.infos.name} in the city whose code is {item.infos.city_code}",
                    )
                area_type_id = AreaTypeRepo.getbyname(self.area, item.infos.area_type).id
                input_code = item.infos.city_code
                maxcode = self.area.maxcodebycityandtype(input_code, area_type_id)
                city_id = CityRepo.getidbycode(self.area, item.infos.city_code)
                zipcode = CityRepo.getbycode(self.area, item.infos.city_code).zipcode
            
            if (place_code is not None) and  (place_code != input_code):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You should only have the list of areas for one city or hirearchical area at a time"
                )

            if (area_type is not None) and (area_type != item.infos.area_type):
                step = 0

            step += 1
            result = Helper.generate_code(
                init_codebase=Helper.area_basecode(input_code),
                maxcode=maxcode,
                step=step
            )
            step = result["step"]
            area_code = result["code"]
            count = self.area.countbycode(code=area_code)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Area already registered with code {area_code}"
                )
                
            if item.infos.is_same_zipcode == False:
                step_zipcode +=1
                zipcode = Helper.generate_zipcode(int(zipcode), step_zipcode)

            agency_id = None
            if (
                hasattr(item.infos, "agency_code") 
                and item.infos.agency_code is not None
            ):
                agency_id = AgencyRepo.getidbycode(self.area, item.infos.agency_code)

            area = CreateArea(
                code = area_code,
                zipcode = zipcode,
                agency_id = agency_id,
                hierarchical_area_id = hierarchical_area_id,
                city_id = city_id,
                area_type_id = area_type_id,
                infos = item.infos
            )
            arealist.append(area)

            if (hasattr(item.infos, "hierarchical_area_code") and item.infos.hierarchical_area_code is not None):
                place_code = item.infos.hierarchical_area_code
            elif (hasattr(item.infos, "city_code") and item.infos.city_code is not None):
                place_code = item.infos.city_code
            
            area_type = item.infos.area_type

        return self.area.create(data=arealist)

    # update area function
    async def update(self, code: int, tokendata: dict, data: AreaUpdate) -> AreaModel:
        old_data = jsonable_encoder(self.area.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Area not found",
            )
        no_hirearchical_type = AreaTypeRepo.no_hierarchical_type(self.area)
        
        if (hasattr(data.infos, "agency_code") and data.infos.agency_code is not None):
            data.agency_id = AgencyRepo.getidbycode(self.area, data.infos.agency_code)
        
        area_type = AreaTypeRepo.get(self.area, old_data["area_type_id"]).name
        
        if (hasattr(data.infos, "area_type") and data.infos.area_type is not None):
            area_type_id = AreaTypeRepo.getbyname(self.area, data.infos.area_type).id
            area_type = data.infos.area_type
            if area_type_id != old_data["area_type_id"]:
                data.area_type_id = area_type_id
            
        if (hasattr(data.infos, "hierarchical_area_code") 
            and data.infos.hierarchical_area_code is not None
            and str(area_type).lower() not in no_hirearchical_type
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The area type must be in {no_hirearchical_type}"
            )
        
        if (hasattr(data.infos, "hierarchical_area_code") 
            and data.infos.hierarchical_area_code is not None
            and str(area_type).lower() in no_hirearchical_type
        ):
            hierachical_area = self.area.getbycode(code=data.infos.hierarchical_area_code)
            hierarchical_area_id = hierachical_area.id
            if hierarchical_area_id != old_data["hierarchical_area_id"]:
                data.hierarchical_area_id = hierarchical_area_id
                data.zipcode = hierachical_area.zipcode
        
        if (hasattr(data.infos, "city_code") and data.infos.city_code is not None):
            city_id = CityRepo.getidbycode(self.area, data.infos.city_code)
            if (data.city_id != old_data["city_id"] and hasattr(data.infos, "is_same_zipcode")):
                data.city_id = city_id
                if data.infos.is_same_zipcode == True:
                    data.zipcode = CityRepo.get(self.area, data.city_id ).zipcode
                else:
                    step_zipcode +=1
                    maxzipcode = AreaRepo.maxzipcodebycity(city_id=city_id).zipcode
                    data.zipcode = Helper.generate_zipcode(maxzipcode, step_zipcode)
        
        current_data = jsonable_encoder(self.area.update(code=code, data=data.dict()))
        logs = [await Helper.build_log(f"/areas/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # activate or desactivate agency function
    async def activate_desactivate(self, code: int, flag: bool, tokendata: dict) -> None:
        old_data = jsonable_encoder(self.area.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agency not found"
            )
        message = "Agency desactivated"
        deleted_at = datetime.utcnow().isoformat()
        
        if flag == True:
            deleted_at = None
            message = "Agency activated"
        
        data = dict(
            is_activated = flag,
            deleted_at = deleted_at
        )
        current_data = jsonable_encoder(self.area.update(code=code, data=data))
        logs = [await Helper.build_log(f"/areas/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return HTTPException(status_code=status.HTTP_200_OK, detail=message)