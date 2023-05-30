from typing import List
from datetime import datetime
from api.tools.Helper import generate_zone_code
from fastapi import Depends, HTTPException, status
from api.ageographical.models.NaturalZoneModel import ZoneModel
from api.ageographical.repositories.NaturalZoneRepo import ZoneRepo
from api.ageographical.schemas.NaturalZoneSchema import (
    ZoneInput,
    ZoneUpdate,
    CreateZone,
)

#
class ZoneService:
    zone: ZoneRepo

    def __init__(self, zone: ZoneRepo = Depends()) -> None:
        self.zone = zone

    # get all natural regions function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[ZoneModel]:
        return self.zone.list(skip=skip, limit=limit)

    # get natural region by id function
    async def get(self, id: int) -> ZoneModel:
        return self.zone.get(id=id)

    # get natural region by code function
    async def getbycode(self, code: str) -> ZoneModel:
        return self.zone.getbycode(code=code)

    # get natural region by name function
    async def getbyname(self, name: str) -> ZoneModel:
        return self.zone.getbyname(name=name)

    # create natural region function
    async def create(self, data: List[ZoneInput]) -> List[CreateZone]:
        maxcode = self.zone.maxcode()            
        zonelist = []  
        for item in data:
            zone = self.zone.getbycode(code=maxcode)
            if zone:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Natural Region already registered with code " + str(maxcode),
                )

            zone = self.zone.getbyname(name=item.name)
            if zone:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Natural Region already registered with name " + str(item.name),
                )
            maxcode = generate_zone_code(maxcode)
            zone = CreateZone(
                name = item.name,
                code = maxcode
            )
            zonelist.append(zone)

        return self.zone.create(data=zonelist)

    # update natural region function
    async def update(self, code: int, data: ZoneUpdate) -> ZoneModel:
        zone = self.zone.getbycode(code=code)
        if zone is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Natural Region not found",
            )

        zone = CreateZone(
            name = data.name,
            code = code
        )
        zonedict = zone.dict(exclude_unset=True)
        for key, val in zonedict.items():
            setattr(zone, key, val)
        return self.zone.update(data=zone)

    # activate or desactivate natural region function
    async def activate_desactivate(self, code: int, flag: bool) -> None:
        zone = self.zone.getbycode(code=code)
        if zone is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Natural Region not found",
            )
        zone.is_activated = flag
        message = "Natural Region desactivated"
        zone.deleted_at = datetime.utcnow().isoformat()
        if flag == True:
            zone.deleted_at = None
            message = "Natural Region activated"

        self.zone.update(data=zone)
        return HTTPException(
            status_code=status.HTTP_200_OK, detail=message
        )
