from typing import List
from datetime import datetime
from api.tools.Helper import build_log
from fastapi.encoders import jsonable_encoder
from api.logs.repositories.LogRepo import LogRepo
from fastapi import Depends, HTTPException, status
from api.electrical.repositories.MeterTypeRepo import MeterTypeRepo
from api.electrical.repositories.SupplyModeRepo import SupplyModeRepo
from api.electrical.models.ElectricMeterModel import ElectricMeterModel
from api.electrical.repositories.ElectricMeterRepo import ElectricMeterRepo
from api.electrical.schemas.ElectricMeterSchema import (
    ElectricMeterInput,
    ElectricMeterUpdate,
    CreateElectricMeter,
)

#
class ElectricMeterService:
    log: LogRepo
    meter: ElectricMeterRepo
    
    def __init__(
        self,
        log: LogRepo = Depends(),
        meter: ElectricMeterRepo = Depends()
    ) -> None:
        self.log = log
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
                    detail="Electric Meter already registered with number " +
                    str(item.meter_number),
                )

            meter = CreateElectricMeter(
                meter_number=item.meter_number,
                meter_type_id=MeterTypeRepo.getbyname(self.meter, item.infos.meter_type).id,
                supply_mode_id=SupplyModeRepo.getbyname(self.meter, item.infos.supply_mode).id,
                infos=item.infos
            )
            metriclist.append(meter)

        return self.meter.create(data=metriclist)

    # update electric meter function
    async def update(self, number: str, data: ElectricMeterUpdate) -> ElectricMeterModel:
        old_data = jsonable_encoder(self.meter.getbynumber(number=number))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Electric Meter not found",
            )

        meter_type_id, supply_mode_id = 0, 0
        if (hasattr(data.infos, "meter_type") and data.infos.meter_type is not None):
            try:
                meter_type_id = MeterTypeRepo.getbyname(self.meter, data.infos.meter_type).id
            except Exception as e:
                raise HTTPException(status_code = 404, detail = "Meter Type not found")

        if (hasattr(data.infos, "supply_mode") and data.infos.supply_mode is not None):
            try:
                supply_mode_id = SupplyModeRepo.getbyname(self.meter, data.infos.supply_mode).id
            except Exception as e:
                raise HTTPException(status_code = 404, detail = "Supply Mode not found")

        verif = self.meter.verif_duplicate(data.meter_number, "ElectricMeterModel.id != " + str(old_data['id']))
        if len(verif) != 0:
            raise HTTPException(status_code=405, detail={"msg": "Duplicates are not possible", "meter_number ": data.meter_number})

        data = data.dict()
        data.update({"meter_type_id": meter_type_id, "supply_mode_id": supply_mode_id, })

        current_data = jsonable_encoder(self.meter.update(number=number, data=data))
        logs = [await build_log(f"/meters/{number}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        self.log.create(logs)
        return current_data
    
    # activate or desactivate electric meter function
    async def activate_desactivate(self, number: str, flag: bool) -> None:
        old_data = jsonable_encoder(self.meter.getbynumber(number=number))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Electric Meter not found",
            )
        message = "Electric Meterdesactivated"
        deleted_at = datetime.utcnow().isoformat()
        
        if flag == True:
            deleted_at = None
            message = "Electric Meter activated"
        
        data = dict(
            is_activated=flag,
            deleted_at = deleted_at
        )
        current_data = jsonable_encoder(self.meter.update(number=number, data=data))
        logs = [await build_log(f"/meters/{number}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        self.log.create(logs)
        return HTTPException(status_code=status.HTTP_200_OK, detail=message)

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
