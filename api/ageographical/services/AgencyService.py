from typing import List
from api.tools.Helper import agency_basecode
from fastapi import Depends, HTTPException, status
from api.ageographical.models.AgencyModel import AgencyModel
from api.ageographical.repositories.AgencyRepo import AgencyRepo
from api.ageographical.schemas.AgencySchema import (
    AgencyBase,
    CreateAgency,
)


class AgencyService:
    agency: AgencyRepo

    def __init__(
        self, agency: AgencyRepo = Depends()
    ) -> None:
        self.agency = agency

    # get all agencys function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[AgencyModel]:
        return self.agency.list(skip=skip, limit=limit)

    # get agency by id function
    async def get(self, id: int) -> AgencyModel:
        return self.agency.get(id=id)

    # get agency by code function
    async def getbycode(self, code: str) -> AgencyBase:
        return self.agency.getbycode(code=code)

    # get agency by name function
    async def getbyname(self, name: str) -> AgencyBase:
        return self.agency.getbyname(name=name)

    # create agency function
    async def create(
        self, data: List[CreateAgency]
    ) -> List[CreateAgency]:
        for item in data:
            item.code = agency_basecode(item.infos)
            agency = self.agency.getbycode(code=item.code)
            if agency:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Agency already registered with code "
                    + str(item.code),
                )

            agency = self.agency.getbyname(
                name=item.infos.name
            )
            if agency:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Agency already registered with name "
                    + item.infos.name,
                )

        return self.agency.create(data=data)

    # update agency function
    async def update(
        self, code: int, data: AgencyBase
    ) -> AgencyModel:
        agency = self.agency.get(code=code)
        if agency is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agency not found",
            )

        agencydict = data.dict(exclude_unset=True)
        for key, val in agencydict.items():
            setattr(agency, key, val)
        return self.agency.update(agency)

    # delete agency function
    async def delete(self, agency: AgencyModel) -> None:
        agency = self.agency.get(id=id)
        if agency is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agency not found",
            )

        self.agency.update(agency)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Agency deleted",
        )
