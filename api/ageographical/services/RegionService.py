from typing import List
from datetime import datetime
from api.tools.Helper import region_basecode
from fastapi import Depends, HTTPException, status
from api.ageographical.models.RegionModel import RegionModel
from api.ageographical.repositories.RegionRepo import RegionRepo
from api.ageographical.repositories.NaturalZoneRepo import ZoneRepo
from api.ageographical.schemas.RegionSchema import (
    RegionInput,
    RegionUpdate,
    CreateRegion,
)

#
class RegionService:
    region: RegionRepo

    def __init__(
        self, region: RegionRepo = Depends()
    ) -> None:
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
        zone_code = 0
        regionlist = []
        for item in data:
            region = self.region.getbyname(name=item.infos.name)
            if region:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Administrative Region already registered with name " + str(item.infos.name),
                )

            maxcode = self.region.maxcodebyzone(item.infos.zone_code)

            step += 1
            region_code = generate_code(
                init_codebase=region_basecode(item.infos.zone_code),
                maxcode=self.region.maxcodebyzone(item.infos.zone_code),
                input_code=item.infos.prefecture_code,
                code=zone_code,
                current_step=step,
                init_step=1
            )
            
            region = self.region.getbycode(region_code)
            if region:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Administrative Region already registered with code " + str(region_code),
                )

            region = CreateRegion(
                code = region_code,
                zone_id = ZoneRepo.getidbycode(self.region, item.infos.zone_code),
                infos = item.infos
            )
            regionlist.append(region)
            zone_code = item.infos.zone_code

        return self.region.create(data=regionlist)

    # update region function
    async def update(self, code: int, data: RegionUpdate) -> RegionModel:
        region = self.region.getbycode(code=code)
        if region is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrative Region not found",
            )

        region = CreateRegion(
            code = code,
            zone_id = ZoneRepo.getidbycode(self.region, data.infos.zone_code),
            infos = data.infos
        )

        regiondict = region.dict(exclude_unset=True)
        for key, val in regiondict.items():
            setattr(region, key, val)
        return self.region.update(region)

    # activate or desactivate region function
    async def activate_desactivate(self, code: int, flag: bool) -> None:
        region = self.region.getbycode(code=code)
        if region is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrative Region not found",
            )
        region.is_activated = flag
        message = "Administrative Region desactivated"
        region.deleted_at = datetime.utcnow().isoformat()
        if flag == True:
            region.deleted_at = None
            message = "Administrative Region activated"

        self.region.update(region)
        return HTTPException(
            status_code=status.HTTP_200_OK, detail=message
        )
