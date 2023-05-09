from typing import List
from api.tools.Helper import supply_basecode
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
    supply: EnergySupplyLineRepo

    def __init__(
        self, supply: EnergySupplyLineRepo = Depends()
    ) -> None:
        self.supply = supply

    # get all energy supplies function
    async def list(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[EnergySupplyLineModel]:
        return self.supply.list(skip=skip, limit=limit)

    # get energy supply line by id function
    async def get(self, id: int) -> EnergySupplyLineModel:
        return self.supply.get(id=id)

    # get energy supply line by code function
    async def getbycode(self, code: str) -> EnergySupplyLineModel:
        return self.supply.getbycode(code=code)

    # get energy supply line by name function
    async def getbyname(self, name: str) -> EnergySupplyLineModel:
        return self.supply.getbyname(name=name)

    # create energy supply line function
    async def create(self, data: List[EnergySupplyLineInput]) -> List[CreateEnergySupplyLine]:
        step = 0
        departure_city_code = 0
        supplylist = []
        for item in data:
            count = self.supply.checklinename(departure_city_code = item.infos.departure_city_code, name=item.infos.name)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Energy Departure already registered with name " + item.infos.name,
                )

            step += 1
            supply_code = generate_code(
                init_codebase=supply_basecode(item.infos.prefecture_code),
                maxcode=self.supply.maxcodebycity(item.infos.departure_city_code),
                input_code=item.infos.departure_city_code,
                code=departure_city_code,
                current_step=step,
                init_step=1
            )

            count = self.supply.countbycode(code=supply_code)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Energy Departure already registered with code " + str(supply_code),
                )
            
            departure_city_id = CityRepo.getidbycode(self.supply, item.infos.departure_city_code)
            arrival_city_id = departure_city_id
            if (hasattr(item.infos, "arrival_city_code") and item.infos.arrival_city_code is not None):
                arrival_city_id = CityRepo.getidbycode(self.supply, item.infos.arrival_city_code)

            supply = CreateEnergySupplyLine(
                code = supply_code,
                departure_city_id = departure_city_id,
                arrival_city_id = arrival_city_id,
                line_type_id = SupplyLineTypeRepo.getbyname(self.supply, item.infos.line_type).id,
                infos = item.infos
            )
            supplylist.append(supply)
            departure_city_code = item.infos.departure_city_code
        
        return self.supply.create(data=supplylist)

    # update energy supply line function
    async def update(self, code: int, data: EnergySupplyLineModel) -> EnergySupplyLineModel:
        count = self.supply.countbycode(code=code)
        if count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Energy Departure not found",
            )
        
        olddata = self.supply.getbycode(code=code)
        departure_city_id = CityRepo.getidbycode(self.supply, item.infos.departure_city_code)
        arrival_city_id = departure_city_id
        if (hasattr(item.infos, "arrival_city_code") and item.infos.arrival_city_code is not None):
            arrival_city_id = CityRepo.getidbycode(self.supply, item.infos.arrival_city_code)

        supply = CreateEnergySupplyLine(
            code = code,
            departure_city_id = departure_city_id,
            arrival_city_id = arrival_city_id,
            line_type_id = SupplyLineTypeRepo.getbyname(self.supply, data.infos.line_type).id,
            infos = data.infos
        )

        supplydict = data.dict(exclude_unset=True)
        for key, val in supplydict.items():
            setattr(supply, key, val)
        return self.supply.update(supply)

    # delete energy supply line function
    async def delete(self, supply: EnergySupplyLineModel) -> None:
        supply = self.supply.get(id=id)
        if supply is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Energy Departure not found",
            )

        self.supply.update(supply)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Energy Departure deleted",
        )
