from typing import List
from datetime import datetime
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from api.logs.services.LogService import LogService
from api.ageographical.repositories.AreaRepo import AreaRepo
from api.ageographical.services.AreaService import AreaService
from api.ageographical.services.CityService import CityService
from api.electrical.services.TransformerService import TransformerService
from api.ageographical.services.PrefectureService import PrefectureService
from api.ageographical.models.DeliveryPointModel import DeliveryPointModel
from api.electrical.repositories.ConnectionPoleRepo import ConnectionPoleRepo
from api.electrical.services.ConnectionPoleService import ConnectionPoleService
from api.ageographical.repositories.DeliveryPointRepo import DeliveryPointRepo
from api.ageographical.schemas.DeliveryPointSchema import (
    CreateDeliveryPoint,
    DeliveryPointUpdate,
    DeliveryPointSchema,
    DeliveryPointDetails
)

#
class DeliveryPointService:
    log: LogService
    area: AreaService
    city: CityService
    prefecture: PrefectureService
    transfomer: TransformerService
    deliverypoint: DeliveryPointRepo
    connectionpole: ConnectionPoleService

    def __init__(
        self,
        log: LogService = Depends(),
        area: AreaService = Depends(),
        city: CityService = Depends(),
        prefecture: PrefectureService = Depends(),
        transformer: TransformerService = Depends(),
        deliverypoint: DeliveryPointRepo = Depends(),
        connectionpole: ConnectionPoleService = Depends()
    ) -> None:
        self.log = log
        self.area = area
        self.city = city
        self.prefecture = prefecture
        self.transformer = transformer
        self.deliverypoint = deliverypoint
        self.connectionpole = connectionpole

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
    async def getbynumber(self, number: int) -> DeliveryPointSchema:
       return self.deliverypoint.getbynumber(number=number)

    # get details of delivery point by number function
    async def getdetails(self, number: int) -> DeliveryPointDetails:
        delivery = self.deliverypoint.getbynumber(number=number)
        
        area = await self.area.getbycode(delivery.infos['area_code'])
        city = await self.city.getbycode(area.infos["city_code"])
        prefecture = await self.prefecture.getbycode(city.infos["prefecture_code"])
        connectionpole = await self.connectionpole.getbynumber(delivery.infos["pole_number"])
        transformer = await self.transformer.getbycode(connectionpole.infos["transformer_code"])

        details = {
            "area": {"code": area.code, "name": f"{area.infos['area_type']} {area.infos['name']}"},
            "city": {"code": city.code, "name": f"{city.infos['city_type']} de {city.infos['name']}"},
            "prefecture": {"code": prefecture.code, "name": prefecture.name},
            "connection_point": {"number": connectionpole.pole_number},
            "transformater": {"code": transformer.transformer_code, "energy_supply_lines": transformer.infos["energy_supply_lines"]}
        }

        deliverypoint = DeliveryPointDetails(
            delivery_point_number = delivery.delivery_point_number,
            infos = delivery.infos,
            details = details
        )
        return deliverypoint

    # create delivery point function
    async def create(self, data: List[CreateDeliveryPoint]) -> List[CreateDeliveryPoint]:
        area_code = None
        deliverypointlist = []
        for item in data:
            if (area_code is not None) and  (area_code != item.infos.area_code):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You should only have the list of delivery point for one area or at a time"
                )
            
            if (area_code is not None) and  (area_code != item.infos.area_code):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You should only have the list of agencies for one city or at a time"
                )

            result = Helper.generate_code(
                init_codebase=Helper.deliverypoint_basecode(item.infos.area_code),
                maxcode=self.deliverypoint.maxnumberyarea(item.infos.area_code),
                step=item.infos.number
            )
            
            delivery_point_number = result["code"]
            count = self.deliverypoint.countbynumber(number=delivery_point_number)

            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Delivery point already registered with code {delivery_point_number}",
                )

            deliverypoint = CreateDeliveryPoint(
                delivery_point_number = delivery_point_number,
                area_id = AreaRepo.getidbycode(self.deliverypoint, item.infos.area_code),
                pole_id = ConnectionPoleRepo.getbynumber(self.deliverypoint, item.infos.pole_number).id,
                infos = item.infos
            )
            
            deliverypointlist.append(deliverypoint)
            area_code = item.infos.area_code

        return self.deliverypoint.create(data=deliverypointlist)

    # update delivery point function
    async def update(self, number: int, tokendata: dict, data: DeliveryPointUpdate) -> DeliveryPointModel:
        old_data = jsonable_encoder(self.deliverypoint.getbynumber(number=number))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Delivery Point not found",
            )

        if (hasattr(data.infos, "area_code") and data.infos.area_code is not None):
            data.area_id = AreaRepo.getidbycode(self.deliverypoint, data.infos.area_code)
            
        if (hasattr(data.infos, "pole_number") and data.infos.pole_number is not None):
            data.pole_id = ConnectionPoleRepo.getbynumber(self.deliverypoint, data.infos.pole_number).id
             
        current_data = jsonable_encoder(self.deliverypoint.update(number, data=data.dict()))
        logs = [await Helper.build_log(f"/deliverypoints/{number}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # activate or desactivate agency function
    async def activate_desactivate(self, number: int, flag: bool, tokendata: dict) -> None:
        old_data = jsonable_encoder(self.deliverypoint.getbynumber(number==number))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Delivery Point not found"
            )
        message = "Delivery Point desactivated"
        deleted_at = datetime.utcnow().isoformat()
        
        if flag == True:
            deleted_at = None
            message = "Delivery Point activated"
        
        data = dict(
            is_activated = flag,
            deleted_at = deleted_at
        )
        current_data = jsonable_encoder(self.deliverypoint(number=number, data=data))
        logs = [await Helper.build_log(f"/deliverypoints/{number}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return HTTPException(status_code=status.HTTP_200_OK, detail=message)