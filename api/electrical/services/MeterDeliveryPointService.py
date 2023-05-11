from typing import List
from fastapi import Depends, HTTPException, status
from api.electrical.models.MeterDeliveryPointModel import MeterDeliveryPointModel
from api.electrical.repositories.MeterDeliveryPointRepo import MeterDeliveryPointRepo
from api.electrical.schemas.MeterDeliveryPointSchema import (
    MeterDeliveryPointBase,
    CreateMeterDeliveryPoint,
)


#
class MeterDeliveryPointService:
    meterdelivery: MeterDeliveryPointRepo

    def __init__(
        self,
        meterdelivery: MeterDeliveryPointRepo = Depends(),
    ) -> None:
        self.meterdelivery = meterdelivery

    # get all meter delivery points function
    async def list(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[MeterDeliveryPointModel]:
        return self.meterdelivery.list(skip=skip, limit=limit)

    # get meter delivery point by id function
    async def get(self, id: int) -> MeterDeliveryPointModel:
        return self.meterdelivery.get(id=id)

    # get by electric meter number function
    async def getbymeternumber(self, number: str) -> MeterDeliveryPointBase:
        return self.meterdelivery.getbymeternumber(number=number)

    # get by delivery point number function
    async def getbydeliverypointnumber(
        self, 
        number: str
    ) -> MeterDeliveryPointBase:
        return self.meterdelivery.getbydeliverypointnumber(number=number)

    # create meter delivery point function
    async def create(
        self, 
        data: List[CreateMeterDeliveryPoint]
    ) -> List[CreateMeterDeliveryPoint]:
        for item in data:
            meterdelivery = self.meterdelivery.getbycode(
                code=item.code
            )
            if meterdelivery:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Meter Delivery Point already registered with code "
                    + str(item.code),
                )

            meterdelivery = self.meterdelivery.getbyname(
                name=item.name
            )
            if meterdelivery:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Meter Delivery Point already registered with name "
                    + item.name,
                )

        return self.meterdelivery.create(data=data)

    # delete meter delivery point function
    async def delete(
        self, 
        meterdelivery: MeterDeliveryPointModel
    ) -> None:
        meterdelivery = self.meterdelivery.get(id=id)
        if meterdelivery is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meter Delivery Point not found",
            )

        self.meterdelivery.update(meterdelivery)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Meter Delivery Point deleted",
        )