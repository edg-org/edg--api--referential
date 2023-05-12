from typing import List
from fastapi import Depends, HTTPException, status
from api.electrical.models.DeliveryPointModel import DeliveryPointModel
from api.electrical.repositories.DeliveryPointRepo import DeliveryPointRepo
from api.electrical.schemas.DeliveryPointSchema import (
    DeliveryPointBase,
    CreateDeliveryPoint,
)


#
class DeliveryPointService:
    deliverypoint: DeliveryPointRepo

    def __init__(
        self,
        deliverypoint: DeliveryPointRepo = Depends(),
    ) -> None:
        self.deliverypoint = deliverypoint

    # get all delivery points function
    async def list(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[DeliveryPointModel]:
        return self.deliverypoint.list(skip=skip, limit=limit)

    # get delivery point by id function
    async def get(self, id: int) -> DeliveryPointModel:
        return self.deliverypoint.get(id=id)

    # get delivery point by number function
    async def getbynumber(self, number: int) -> DeliveryPointBase:
        return self.deliverypoint.getbynumber(number=number)

    # get delivery point by name function
    async def getbyname(self, name: str) -> DeliveryPointBase:
        return self.deliverypoint.getbyname(name=name)

    # create delivery point function
    async def create(self, data: List[CreateDeliveryPoint]) -> List[CreateDeliveryPoint]:
        step = 0
        pointlist = []
        area_code = None
        for item in data:
            if (area_code is not None) and  (area_code != item.infos.area_code):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You should only have the list of delivery point for one area or at a time"
                )
            
            step += 1
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
                    detail="Agency already registered with code "
                    + str(item.code),
                )
            agency = CreateAgency(
                code = agency_code,
                city_id = CityRepo.getidbycode(self.agency, item.infos.city_code),
                infos = item.infos
            )
            agencylist.append(agency)
            city_code = item.infos.city_code

        return self.deliverypoint.create(data=data)

    # update delivery point function
    async def update(self, number: int, data: DeliveryPointBase) -> DeliveryPointModel:
        deliverypoint = self.deliverypoint.getbynumber(
            number=number
        )
        if deliverypoint is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Delivery Point not found",
            )

        deliverypointdict = data.dict(exclude_unset=True)
        for key, val in deliverypointdict.items():
            setattr(deliverypoint, key, val)
        return self.deliverypoint.update(deliverypoint)

    # delete delivery point function
    async def delete(self, deliverypoint: DeliveryPointModel) -> None:
        deliverypoint = self.deliverypoint.get(id=id)
        if deliverypoint is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Delivery Point not found",
            )

        self.deliverypoint.update(deliverypoint)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Delivery Point deleted",
        )
