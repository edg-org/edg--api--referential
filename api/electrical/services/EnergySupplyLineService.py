from typing import List
from fastapi import Depends, HTTPException, status
from api.ageographical.repositories.CityRepo import CityRepo
from api.tools.Helper import generate_code, energy_supply_basecode
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
        self, energysupply: EnergySupplyLineRepo = Depends()
    ) -> None:
        self.energysupply = energysupply

    # get all energy supplies function
    async def list(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[EnergySupplyLineModel]:
        return self.energysupply.list(skip=skip, limit=limit)

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
                    detail="Energy Departure already registered with name " + item.infos.name,
                )

            if (city_code is not None) and  (city_code != item.infos.departure_city_code):
                step = 0
                
            step += 1
            line_type_id = SupplyLineTypeRepo.getbyname(self.energysupply, item.infos.line_type).id
            departure_city_code = item.infos.departure_city_code
            suffix = (departure_city_code*10)+line_type_id
            result = generate_code(
                init_codebase=energy_supply_basecode(suffix),
                maxcode=self.energysupply.maxcodebycitylinetype(departure_city_code, line_type_id),
                step=step
            )
            step = result["step"]
            energy_supply_code = result["code"]
            count = self.energysupply.countbycode(code=energy_supply_code)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Energy Departure already registered with code " + str(supply_code),
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
        count = self.energysupply.countbycode(code=code)
        if count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Energy Departure not found",
            )
        
        olddata = self.energysupply.getbycode(code=code)
        departure_city_id = CityRepo.getidbycode(self.energysupply, item.infos.departure_city_code)
        arrival_city_id = departure_city_id
        if (hasattr(item.infos, "arrival_city_code") and item.infos.arrival_city_code is not None):
            arrival_city_id = CityRepo.getidbycode(self.energysupply, item.infos.arrival_city_code)

        supply = CreateEnergySupplyLine(
            code = code,
            departure_city_id = departure_city_id,
            arrival_city_id = arrival_city_id,
            line_type_id = SupplyLineTypeRepo.getbyname(self.energysupply, data.infos.line_type).id,
            infos = data.infos
        )

        supplydict = data.dict(exclude_unset=True)
        for key, val in supplydict.items():
            setattr(supply, key, val)
        return self.energysupply.update(supply)

    # delete energy supply line function
    async def delete(self, energy_supply: EnergySupplyLineModel) -> None:
        energy_supply = self.energysupply.get(id=id)
        if energy_supply is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Energy Departure not found",
            )

        self.energysupply.update(energy_supply)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Energy Departure deleted",
        )