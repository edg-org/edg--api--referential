from typing import List
from datetime import datetime
from api.tools.Helper import region_basecode
from fastapi import Depends, HTTPException, status
from api.egeographical.models.RegionModel import RegionModel
from api.egeographical.repositories.RegionRepo import (
    RegionRepo,
)
from api.egeographical.repositories.NaturalZoneRepo import (
    ZoneRepo,
)
from api.egeographical.schemas.RegionSchema import (
    RegionBase,
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
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[RegionModel]:
        return self.region.list(skip=skip, limit=limit)

    # get region by id function
    async def get(self, id: int) -> RegionModel:
        return self.region.get(id=id)

    # get region by code function
    async def getbycode(self, code: str) -> RegionBase:
        return self.region.getbycode(code=code)

    # get region by name function
    async def getbyname(self, name: str) -> RegionBase:
        return self.region.getbyname(name=name)

    # create region function
    async def create(
        self, data: List[CreateRegion]
    ) -> List[CreateRegion]:
        step = 0
        zone_code = 0
        for item in data:
            maxcode = self.region.maxcodebyzone(
                item.infos.zone_code
            )
            if maxcode is None:
                maxcode = 0

            item.zone_id = ZoneRepo.getid_bycode(
                self.region, item.infos.zone_code
            )

            if maxcode > 0:
                step += 1
                basecode = maxcode
            else:
                basecode = region_basecode(
                    item.infos.zone_code
                )
                if zone_code == item.infos.zone_code:
                    step += 1
                else:
                    step = 1

            region_code = basecode + step
            zone_code = item.infos.zone_code
            item.code = region_code

            region = self.region.getbycode(region_code)

            if region:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Administrative Region already registered with code "
                    + str(item.code),
                )

            region = self.region.getbyname(
                name=item.infos.name
            )
            if region:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Administrative Region already registered with name "
                    + str(item.infos.name),
                )

        return self.region.create(data=data)

    # update region function
    async def update(
        self, code: int, data: RegionBase
    ) -> RegionModel:
        region = self.region.getbycode(code=code)
        if region is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrative Region not found",
            )

        regiondict = data.dict(exclude_unset=True)
        for key, val in regiondict.items():
            setattr(region, key, val)
        return self.region.update(region)

    # activate or desactivate region function
    async def activate_desactivate(
        self, id: int, flag: bool
    ) -> None:
        region = self.naturalRegion.get(id=id)
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

        self.naturalRegion.update(region)
        return HTTPException(
            status_code=status.HTTP_200_OK, detail=message
        )
