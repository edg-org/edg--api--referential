import httpx
from typing import List
from api.configs.Environment import get_env_var
from fastapi import Depends, HTTPException, status
from api.ageographical.repositories.AreaRepo import AreaRepo
from api.tools.Helper import deliverypoint_basecode, generate_code
from api.ageographical.models.DeliveryPointModel import DeliveryPointModel
from api.ageographical.repositories.DeliveryPointRepo import DeliveryPointRepo
from api.ageographical.schemas.DeliveryPointSchema import (
    CreateDeliveryPoint,
    DeliveryPointUpdate,
    DeliveryPointSchema,
    DeliveryPointDetails
)

env = get_env_var()
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
    async def getbynumber(self, number: int) -> DeliveryPointSchema:
       return self.deliverypoint.getbynumber(number=number)

    # get details of delivery point by number function
    async def getdetails(self, number: int) -> DeliveryPointDetails:
        client = httpx.AsyncClient()
        baseUrl = env.domaine_name + env.api_routers_prefix + env.api_version
        delivery = self.deliverypoint.getbynumber(number=number)
        area_code = delivery.infos['area_code']
        area = (await client.get(baseUrl+"/areas/"+str(area_code))).json()
        city_code = area["infos"]["city_code"]
        city = (await client.get(baseUrl+"/cities/search?code="+str(city_code))).json()
        prefecture_code = city["infos"]["prefecture_code"]
        prefecture = (await client.get(baseUrl+"/prefectures/"+str(prefecture_code))).json()
       
        details = {
            "area": {"code": area["code"], "name": area["infos"]["area_type"]+" "+ area["infos"]["name"]},
            "city": {"code": city["code"], "name": city["infos"]["city_type"]+" de "+ city["infos"]["name"]},
            "prefecture": {"code": prefecture["code"], "name": prefecture["name"]}
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

            result = generate_code(
                init_codebase=deliverypoint_basecode(item.infos.area_code),
                maxcode=self.deliverypoint.maxnumberyarea(item.infos.area_code),
                step=item.infos.number
            )
            
            delivery_point_number = result["code"]
            count = self.deliverypoint.countbynumber(number=delivery_point_number)

            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Delivery point already registered with code " + str(delivery_point_number),
                )

            deliverypoint = CreateDeliveryPoint(
                delivery_point_number = delivery_point_number,
                area_id = AreaRepo.getidbycode(self.deliverypoint, item.infos.area_code),
                infos = item.infos
            )
            
            deliverypointlist.append(deliverypoint)
            area_code = item.infos.area_code

        return self.deliverypoint.create(data=deliverypointlist)

    # update delivery point function
    async def update(self, number: int, data: DeliveryPointUpdate) -> DeliveryPointModel:
        deliverypoint = self.deliverypoint.getbynumber(number=number)
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
