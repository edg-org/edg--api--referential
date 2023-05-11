from typing import List
from fastapi import Depends, HTTPException, status
from api.electrical.repositories.PowerModeRepo import PowerModeRepo
from api.electrical.repositories.MeterTypeRepo import MeterTypeRepo
from api.electrical.models.ElectricMeterModel import ElectricMeterModel
from api.electrical.repositories.ElectricMeterRepo import ElectricMeterRepo
from api.electrical.schemas.ElectricMeterSchema import (
    ElectricMeterInput,
    ElectricMeterUpdate,
    CreateElectricMeter,
)


#
class ElectricMeterService:
    meter: ElectricMeterRepo

    def __init__(
        self,
        meter: ElectricMeterRepo = Depends(),
    ) -> None:
        self.meter = meter

    # get all electric meters function
    async def list(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ElectricMeterModel]:
        return self.meter.list(skip=skip, limit=limit)

    # get electric meter by id function
    async def get(self, id: int) -> ElectricMeterModel:
        return self.meter.get(id=id)

    # get electric meter by number function
    async def getbynumber(self, number: str) -> ElectricMeterModel:
        return self.meter.getbynumber(number=number)

    # create electric meter function
    async def create(self, data: List[ElectricMeterInput]) -> List[CreateElectricMeter]:
        metriclist = []
        for item in data:
            count = self.meter.countbynumber(number=item.meter_number)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Electric Meter already registered with number " + str(item.meter_number),
                )
            
            meter = CreateElectricMeter(
                meter_number = item.meter_number,
                meter_type_id = MeterTypeRepo.getbyname(self.meter, item.infos.meter_type).id,
                power_mode_id = PowerModeRepo.getbyname(self.meter, item.infos.power_mode).id,
                infos = item.infos
            )
            metriclist.append(meter)

        return self.meter.create(data=metriclist)

    # update electric meter function
    async def update(self, number: int, data: ElectricMeterUpdate) -> ElectricMeterModel:
        meter = self.meter.getbynumber(number=number)
        if meter is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Electric Meter not found",
            )

        meterdict = data.dict(exclude_unset=True)
        for key, val in meterdict.items():
            setattr(meter, key, val)
        return self.meter.update(meter)

    # delete electric meter function
    async def delete(self, meter: ElectricMeterModel) -> None:
        meter = self.meter.get(id=id)
        if meter is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Electric Meter not found",
            )

        self.meter.update(meter)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Electric Meter deleted",
        )