from typing import List
from datetime import datetime
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from api.logs.repositories.LogRepo import LogRepo
from fastapi import Depends, HTTPException, status
from api.ageographical.repositories.CityRepo import CityRepo
from api.ageographical.models.AgencyModel import AgencyModel
from api.ageographical.repositories.AgencyRepo import AgencyRepo
from api.ageographical.schemas.AgencySchema import (
    AgencyInput,
    AgencyUpdate,
    CreateAgency
)

#
class AgencyService:
    log: LogRepo
    agency: AgencyRepo

    def __init__(
        self, 
        log: LogRepo = Depends(),
        agency: AgencyRepo = Depends()
    ) -> None:
        self.log = log
        self.agency = agency

    # get all agencys function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[AgencyModel]:
        return self.agency.list(skip=skip, limit=limit)

    # get agency by code function
    async def getbycode(self, code: str) -> AgencyModel:
        return self.agency.getbycode(code=code)

    # get agency by name function
    async def getbyname(self, name: str) -> AgencyModel:
        return self.agency.getbyname(name=name)

    # create agency function
    async def create(self, data: List[AgencyInput]) -> List[CreateAgency]:
        step = 0
        city_code = None
        agencylist = []
        for item in data:
            count = self.agency.countbyname(name=item.infos.name)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Agency already registered with name {item.infos.name}",
                )
            
            if (city_code is not None) and (city_code != item.infos.city_code):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You should only have the list of agencies for one city or at a time"
                )

            step += 10
            result = Helper.generate_code(
                init_codebase=Helper.agency_basecode(item.infos.city_code),
                maxcode=self.agency.maxcodebycity(item.infos.city_code),
                step=step
            )
            step = result["step"]
            agency_code = result["code"]
            count = self.agency.countbycode(code=agency_code)

            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Agency already registered with code {agency_code}",
                )
            agency = CreateAgency(
                code = agency_code,
                city_id = CityRepo.getidbycode(self.agency, item.infos.city_code),
                infos = item.infos
            )
            agencylist.append(agency)
            city_code = item.infos.city_code

        return self.agency.create(data=agencylist)

    # update agency function
    async def update(self, code: int, tokendata: dict, data: AgencyUpdate) -> AgencyModel:
        old_data = jsonable_encoder(self.agency.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agency not found",
            )

        if (hasattr(data.infos, "city_id") and data.infos.city_id is None):
            data.city_id = CityRepo.getidbycode(self.agency, data.infos.city_code)
            
        current_data = jsonable_encoder(self.agency.update(code=code, data=data.dict()))
        logs = [await Helper.build_log(f"/agencies/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return current_data

        
    # activate or desactivate agency function
    async def activate_desactivate(self, code: int, flag: bool, tokendata: dict) -> None:
        old_data = jsonable_encoder(self.agency.getbycode(code=code))
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
        current_data = jsonable_encoder(self.agency.update(code=code, data=data))
        logs = [await Helper.build_log(f"/agencies/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return HTTPException(status_code=status.HTTP_200_OK, detail=message)