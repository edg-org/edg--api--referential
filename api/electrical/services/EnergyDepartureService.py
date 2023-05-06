from typing import List
from fastapi import Depends, HTTPException, status
from api.electrical.models.EnergyDepartureModel import (
    EnergyDepartureModel,
)
from api.electrical.repositories.EnergyDepartureRepo import (
    EnergyDepartureRepo,
)
from api.electrical.schemas.EnergyDepartureSchema import (
    EnergyDepartureBase,
    CreateEnergyDeparture,
)


#
class EnergyDepartureService:
    departure: EnergyDepartureRepo

    def __init__(
        self, departure: EnergyDepartureRepo = Depends()
    ) -> None:
        self.departure = departure

    # get all energy departures function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[EnergyDepartureModel]:
        return self.departure.list(skip=skip, limit=limit)

    # get energy departure by id function
    async def get(self, id: int) -> EnergyDepartureModel:
        return self.departure.get(id=id)

    # get energy departure by code function
    async def getbycode(
        self, code: str
    ) -> EnergyDepartureBase:
        return self.departure.getbycode(code=code)

    # get energy departure by name function
    async def getbyname(
        self, name: str
    ) -> EnergyDepartureBase:
        return self.departure.getbyname(name=name)

    # create energy departure function
    async def create(
        self, data: List[CreateEnergyDeparture]
    ) -> List[CreateEnergyDeparture]:
        for item in data:
            departure = self.departure.getbycode(
                code=item.code
            )
            if departure:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Energy Departure already registered with code "
                    + str(item.code),
                )


            departure = self.departure.getbyname(
                name=item.infos.name
            )
            if departure:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Energy Departure already registered with name "
                    + item.infos.name,
                )

        return self.departure.create(data=data)

    # update energy departure function
    async def update(
        self, code: int, data: EnergyDepartureBase
    ) -> EnergyDepartureModel:
        departure = self.departure.getbycode(code=code)
        if departure is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Energy Departure not found",
            )

        departuredict = data.dict(exclude_unset=True)
        for key, val in departuredict.items():
            setattr(departure, key, val)
        return self.departure.update(departure)

    # delete energy departure function
    async def delete(
        self, departure: EnergyDepartureModel
    ) -> None:
        departure = self.departure.get(id=id)
        if departure is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Energy Departure not found",
            )

        self.departure.update(departure)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Energy Departure deleted",
        )
