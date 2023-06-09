from typing import List
from datetime import datetime
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from api.logs.services.LogService import LogService
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
    log: LogService

    def __init__(
        self, 
        zone: ZoneRepo = Depends(),
        log: LogService = Depends()
    ) -> None:
        self.log = log
        self.zone = zone

    # get all natural regions function
    async def list(self, start: int = 0, size: int = 100) -> List[ZoneModel]:
        return self.zone.list(start=start, size=size)

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
                    detail=f"Natural Region already registered with code {maxcode}"
                )

            zone = self.zone.getbyname(name=item.name)
            if zone:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Natural Region already registered with name {item.name}"
                )
            maxcode = Helper.generate_zone_code(maxcode)
            zone = CreateZone(
                name = item.name,
                code = maxcode
            )
            zonelist.append(zone)

        return self.zone.create(data=zonelist)

    # update natural region function
    async def update(self, code: int, tokendata: dict, data: ZoneUpdate) -> ZoneModel:
        old_data = jsonable_encoder(self.zone.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Natural Region not found",
            )

        current_data = jsonable_encoder(self.zone.update(code, data=data.dict()))
        logs = [await Helper.build_log(f"/naturalregions/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # activate or desactivate natural region function
    async def activate_desactivate(self, code: int, flag: bool, tokendata: dict) -> None:
        old_data = jsonable_encoder(self.zone.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Natural Region not found"
            )
        message = "Natural Region desactivated"
        deleted_at = datetime.utcnow().isoformat()
        
        if flag == True:
            deleted_at = None
            message = "Natural Region activated"
        
        data = dict(
            is_activated=flag,
            deleted_at = deleted_at
        )
        current_data = jsonable_encoder(self.zone.update(code=code, data=data))
        logs = [await Helper.build_log(f"/naturalregions/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return HTTPException(status_code=status.HTTP_200_OK, detail=message)
