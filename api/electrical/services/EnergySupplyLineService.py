from typing import List
from datetime import datetime
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from api.logs.repositories.LogRepo import LogRepo
from fastapi import Depends, HTTPException, status
from api.ageographical.repositories.CityRepo import CityRepo
from api.electrical.repositories.SupplyLineTypeRepo import SupplyLineTypeRepo
from api.electrical.models.EnergySupplyLineModel import EnergySupplyLineModel
from api.electrical.repositories.EnergySupplyLineRepo import EnergySupplyLineRepo
from api.electrical.schemas.EnergySupplyLineSchema import (
    EnergySupplyLineInput,
    CreateEnergySupplyLine
)

#
class EnergySupplyLineService:
    log: LogRepo
    supply: EnergySupplyLineRepo

    def __init__(
        self, 
        log: LogRepo = Depends(),
        energysupply: EnergySupplyLineRepo = Depends()
    ) -> None:
        self.log = log
        self.energysupply = energysupply

    # get all energy supplies function
    async def list(self, start: int = 0, size: int = 100) -> (int, List[EnergySupplyLineModel]):
        return self.energysupply.list(start=start, size=size)

    # get energy supply line by id function
    async def get(self, id: int) -> EnergySupplyLineModel:
        return self.energysupply.get(id=id)

    # get energy supply line by code function
    async def getbycode(self, code: str) -> EnergySupplyLineModel:
        return self.energysupply.getbycode(code=code)

    # get energy supply line by name function
    async def getbyname(self, name: str) -> EnergySupplyLineModel:
        return self.energysupply.getbyname(name=name)

    # create energy supply line function
    async def create(self, data: List[EnergySupplyLineInput]) -> List[CreateEnergySupplyLine]:
        step = 0
        city_code = None
        energysupplylist = []
        departure_city_code = 0
        for item in data:
            count = self.energysupply.checklinename(departure_city_code = item.infos.departure_city_code, name=item.infos.name)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Energy Departure already registered with name {item.infos.name}",
                )

            if (city_code is not None) and  (city_code != item.infos.departure_city_code):
                step = 0
                
            step += 1
            line_type_id = SupplyLineTypeRepo.getbyname(self.energysupply, item.infos.line_type).id
            departure_city_code = item.infos.departure_city_code
            suffix = (departure_city_code*10)+line_type_id
            result = Helper.generate_code(
                init_codebase=Helper.energy_supply_basecode(suffix),
                maxcode=self.energysupply.maxcodebycitylinetype(departure_city_code, line_type_id),
                step=step
            )
            step = result["step"]
            energy_supply_code = result["code"]
            count = self.energysupply.countbycode(code=energy_supply_code)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Energy Departure already registered with code {energy_supply_code}",
                )
            
            energy_supply = CreateEnergySupplyLine(
                code = energy_supply_code,
                departure_city_id =  CityRepo.getidbycode(self.energysupply, item.infos.departure_city_code),
                line_type_id = line_type_id,
                infos = item.infos
            )
            energysupplylist.append(energy_supply)
            city_code = item.infos.departure_city_code
        
        return self.energysupply.create(data=energysupplylist)

    # update energy supply line function
    async def update(self, code: int, data: EnergySupplyLineModel) -> EnergySupplyLineModel:
        old_data = jsonable_encoder(self.energysupply.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Energy Supply Line not found",
            )
        
        if (hasattr(data.infos, "line_type") and data.infos.line_type is not None):
            data.line_type_id = SupplyLineTypeRepo.getbyname(self.energysupply, data.infos.line_type).id
        
        if (hasattr(data.infos, "departure_city_code") and data.infos.departure_city_code is not None):
            data.departure_city_id = CityRepo.getidbycode(self.energysupply, data.infos.departure_city_code)
            
        current_data = jsonable_encoder(self.energysupply.update(code=code, data=data.dict()))
        logs = [Helper.build_log(f"/supplylines/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # activate or desactivate energy supply line function
    async def activate_desactivate(self, code: int, flag: bool) -> None:
        old_data = jsonable_encoder(self.energysupply.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Energy Supply Line not found",
            )
        message = "Energy Supply Line desactivated"
        deleted_at = datetime.utcnow().isoformat()
        
        if flag == True:
            deleted_at = None
            message = "Energy Supply Line activated"
        
        data = dict(
            is_activated=flag,
            deleted_at = deleted_at
        )
        current_data = jsonable_encoder(self.transformer.update(code=code, data=data))
        logs = [Helper.build_log(f"/supplylines/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        await self.log.create(logs)
        return HTTPException(status_code=status.HTTP_200_OK, detail=message)