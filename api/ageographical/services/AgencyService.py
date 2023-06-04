from typing import List
from api.logs.repositories.LogRepo import LogRepo
from fastapi import Depends, HTTPException, status
from api.tools.Helper import agency_basecode, generate_code
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
            result = generate_code(
                init_codebase=agency_basecode(item.infos.city_code),
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
    async def update(self, code: int, data: AgencyUpdate) -> AgencyModel:
        count = self.agency.countbycode(code=code)
        if count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agency not found",
            )

        agency = CreateAgency(
            code = code,
            city_id = CityRepo.getidbycode(self.agency, data.infos.city_code),
            infos = data.infos
        )
        agencydict = agency.dict(exclude_unset=True)
        for key, val in agencydict.items():
            setattr(agency, key, val)
        return self.agency.update(agency)

    # delete agency function
    async def delete(self, code: int) -> None:
        data = self.agency.getbycode(code=code)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agency not found",
            )

        self.agency.delete(data)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Agency deleted"
        )