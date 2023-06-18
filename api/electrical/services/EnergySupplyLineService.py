from typing import List
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from api.logs.repositories.LogRepo import LogRepo
from fastapi import Depends, HTTPException, status
from api.ageographical.repositories.CityRepo import CityRepo
from api.ageographical.repositories.AreaRepo import AreaRepo
from api.tools.Helper import generate_code, energy_supply_basecode, build_log
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
        energysupply: EnergySupplyLineRepo = Depends(),
        cityrepo: CityRepo = Depends(),
        arearepo: AreaRepo = Depends()
    ) -> None:
        self.log = log
        self.energysupply = energysupply
        self.cityrepo = cityrepo
        self.arearepo = arearepo

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
        area_code = None
        energysupplylist = []
        departure_area_code = 0
        for item in data:
            count = self.energysupply.checklinename(code = item.infos.departure_area_code, name=item.infos.name)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Energy Departure already registered with name {item.infos.name}",
                )

            if (area_code is not None) and  (area_code != item.infos.departure_area_code):
                step = 0

            step += 1
            line_type_id = SupplyLineTypeRepo.getbyname(self.energysupply, item.infos.line_type).id
            departure_area_code = item.infos.departure_area_code
            suffix = (departure_area_code*10)+line_type_id
            result = generate_code(
                init_codebase=energy_supply_basecode(suffix),
                maxcode=self.energysupply.maxcodebycitylinetype(departure_area_code, line_type_id),
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
                line_type_id = line_type_id,
                departure_area_id =  self.arearepo.getidbycode(item.infos.departure_area_code),
                voltage_type_id = 1,
                infos = item.infos
            )
            energysupplylist.append(energy_supply)
            area_code = item.infos.departure_area_code

        return self.energysupply.create(data=energysupplylist)

    # # create energy supply line function
    # async def create(self, data: List[EnergySupplyLineInput]) -> List[CreateEnergySupplyLine]:
    #     step = 0
    #     city_code = None
    #     area_code = None
    #     energysupplylist = []
    #     departure_city_code = 0
    #     for item in data:
    #         count = self.energysupply.checklinename(code = item.infos.departure_area_code, name=item.infos.name)
    #         # count = self.energysupply.checklinename(departure_city_code = item.infos.departure_city_code, name=item.infos.name)
    #         if count > 0:
    #             raise HTTPException(
    #                 status_code=status.HTTP_400_BAD_REQUEST,
    #                 detail=f"Energy Departure already registered with name {item.infos.name}",
    #             )
    #
    #         if (area_code is not None) and  (area_code != item.infos.departure_area_code):
    #             step = 0
    #
    #         # if (city_code is not None) and  (city_code != item.infos.departure_city_code):
    #         #     step = 0
    #
    #         step += 1
    #         line_type_id = SupplyLineTypeRepo.getbyname(self.energysupply, item.infos.line_type).id
    #         departure_city_code = item.infos.departure_city_code
    #         suffix = (departure_city_code*10)+line_type_id
    #         result = generate_code(
    #             init_codebase=energy_supply_basecode(suffix),
    #             maxcode=self.energysupply.maxcodebycitylinetype(departure_city_code, line_type_id),
    #             step=step
    #         )
    #
    #         step = result["step"]
    #         energy_supply_code = result["code"]
    #         count = self.energysupply.countbycode(code=energy_supply_code)
    #         if count > 0:
    #             raise HTTPException(
    #                 status_code=status.HTTP_400_BAD_REQUEST,
    #                 detail=f"Energy Departure already registered with code {energy_supply_code}",
    #             )
    #
    #
    #         energy_supply = CreateEnergySupplyLine(
    #             code = energy_supply_code,
    #             # departure_city_id =  CityRepo.getidbycode(self.energysupply, item.infos.departure_city_code),
    #             departure_city_id = self.cityrepo.getidbycode(item.infos.departure_city_code),
    #             line_type_id = line_type_id,
    #             departure_area_id =  self.arearepo.getidbycode(item.infos.departure_area_code),
    #             # departure_area_id = 9,
    #             voltage_type_id = 1,
    #             infos = item.infos
    #         )
    #         energysupplylist.append(energy_supply)
    #         city_code = item.infos.departure_city_code
    #         area_code = item.infos.departure_area_code
    #
    #     return self.energysupply.create(data=energysupplylist)
    #     # return []

    # update energy supply line function
    async def update(self, code: int, data: EnergySupplyLineModel) -> EnergySupplyLineModel:
        old_data = jsonable_encoder(self.energysupply.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Energy Supply Line not found",
            )
        
        # if (hasattr(data.infos, "line_type") and data.infos.line_type is not None):
        #     data.line_type_id = SupplyLineTypeRepo.getbyname(self.energysupply, data.infos.line_type).id
        #
        # if (hasattr(data.infos, "departure_city_code") and data.infos.departure_city_code is not None):
        #     data.departure_city_id = CityRepo.getidbycode(self.energysupply, data.infos.departure_city_code)
        verif = self.energysupply.verif_duplicate(data.infos.name, "EnergySupplyLineModel.id != " + str(old_data['id']))
        if len(verif) != 0:
            raise HTTPException(status_code=405, detail={"msg": "Duplicates are not possible", "name": data.infos.name})

        current_data = jsonable_encoder(self.energysupply.update(code=code, data=data.dict()))
        logs = [await build_log(f"/supplylines/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        self.log.create(logs)
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
        logs = [build_log(f"/supplylines/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        await self.log.create(logs)
        return HTTPException(status_code=status.HTTP_200_OK, detail=message)
    
    # delete energy supply line function
    async def delete(self, code: int) -> None:
        data = self.energysupply.getbycode(code=code)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Energy Departure not found",
            )

        self.energysupply.delete(data)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Energy Departure deleted",
        )