from typing import List
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from api.logs.services.LogService import LogService
from api.ageographical.models.RegionModel import RegionModel
from api.ageographical.repositories.RegionRepo import RegionRepo
from api.ageographical.repositories.NaturalZoneRepo import ZoneRepo
from api.tools.Helper import region_basecode, generate_code, build_log
from api.ageographical.schemas.RegionSchema import (
    RegionInput,
    RegionUpdate,
    CreateRegion
)

#
class RegionService:
    region: RegionRepo
    log: LogService

    def __init__(
        self, 
        log : LogService = Depends(),
        region: RegionRepo = Depends()
    ) -> None:
        self.log = log
        self.region = region

    # get all regions function
    async def list(self, skip: int = 0, limit: int = 100) -> List[RegionModel]:
        return self.region.list(skip=skip, limit=limit)

    # get region by id function
    async def get(self, id: int) -> RegionModel:
        return self.region.get(id=id)

    # get region by code function
    async def getbycode(self, code: str) -> RegionModel:
        return self.region.getbycode(code=code)

    # get region by name function
    async def getbyname(self, name: str) -> RegionModel:
        return self.region.getbyname(name=name)

    # create region function
    async def create(self, data: List[RegionInput]) -> List[CreateRegion]:
        step = 0
        zone_name = None
        regionlist = []

        for item in data:
            region = self.region.getbyname(name=item.name)
            if region:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Administrative Region already registered with name {item.name}",
                )

            if (zone_name is not None) and  (zone_name != item.infos.natural_zone):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You should only have the list of administrative regions for one natural region at a time"
                )

            step += 1
            natural_zone = ZoneRepo.getbyname(self.region, item.infos.natural_zone)
            result = generate_code(
                init_codebase=region_basecode(natural_zone.code),
                maxcode=self.region.maxcodebyzone(item.infos.natural_zone),
                step=step
            )
            step = result["step"]
            region_code = result["code"]       
            region = self.region.getbycode(region_code)
            if region:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Administrative Region already registered with code {region_code}",
                )

            region = CreateRegion(
                code = region_code,
                name = item.name,
                zone_id = natural_zone.id,
                infos = item.infos
            )
            regionlist.append(region)
            zone_name = item.infos.natural_zone

        return self.region.create(data=regionlist)

    # update region function
    async def update(self, code: int, data: RegionUpdate) -> RegionModel:
        old_data = jsonable_encoder(self.region.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrative Region not found",
            )

        current_data = jsonable_encoder(self.region.update(code, data=data.dict()))
        logs = [build_log(f"/regions/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # activate or desactivate region function
    async def activate_desactivate(self, code: int, flag: bool) -> None:
        old_data = self.region.getbycode(code=code)
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrative Region not found",
            )
        message = "Administrative Region desactivated"
        deleted_at = datetime.utcnow().isoformat()
        
        if flag == True:
            deleted_at = None
            message = "Administrative Region activated"
        
        data = dict(
            is_activated=flag,
            deleted_at = deleted_at
        )
        current_data = jsonable_encoder(self.region.update(code=code, data=data))
        logs = [build_log(f"/regions/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        await self.log.create(logs)
        return HTTPException(status_code=status.HTTP_200_OK, detail=message)