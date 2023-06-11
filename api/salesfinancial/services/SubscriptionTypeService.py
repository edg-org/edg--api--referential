from typing import List
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from api.logs.services.LogService import LogService
from api.electrical.repositories.SupplyModeRepo import SupplyModeRepo
from api.salesfinancial.repositories.TrackingTypeRepo import TrackingTypeRepo
from api.salesfinancial.models.SubscriptionTypeModel import SubscriptionTypeModel
from api.salesfinancial.repositories.SubscriptionTypeRepo import SubscriptionTypeRepo
from api.salesfinancial.schemas.SubscriptionTypeSchema import SubscriptionTypeInput, CreateSubscriptionType

class SubscriptionTypeService:
    log: LogService
    subscriptiontype: SubscriptionTypeRepo

    def __init__(
        self,
        log: LogService = Depends(),
        subscriptiontype: SubscriptionTypeRepo = Depends()
    ) -> None:
        self.log = log
        self.subscriptiontype = subscriptiontype

    # get all subscription types function
    async def list(self, skip: int = 0, limit: int = 100) -> List[SubscriptionTypeModel]:
        return self.subscriptiontype.list(skip=skip, limit=limit)

    # get subscription type by id function
    async def get(self, id: int) -> SubscriptionTypeModel:
        return self.subscriptiontype.get(id=id)

    # get subscription type by code function
    async def getbycode(self, code: str) -> SubscriptionTypeModel:
        return self.subscriptiontype.getbycode(code=code)

    # get subscription type by name function
    async def getbyname(self, name: str) -> SubscriptionTypeModel:
        return self.subscriptiontype.getbyname(name=name)

    # create subscription type function
    async def create(self, data: List[SubscriptionTypeInput]) -> List[CreateSubscriptionType]:
        datalist = []
        for item in data:
            subscriptiontype = self.subscriptiontype.getbycode(code=item.code)
            if subscriptiontype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Subscription Type already registered with code {item.code}"
                )

            subscriptiontype = self.subscriptiontype.getbyname(name=item.name)

            if subscriptiontype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Subscription Type already registered with name {item.name}"
                )

            subscription = CreateSubscriptionType(
                code = item.code,
                name = item.name,
                infos = item.infos,
                pricing = item.pricing,
                dunning = item.dunning,
                supply_mode_id = SupplyModeRepo.getidbyname(self.subscriptiontype, item.infos.supply_mode),
                tracking_type_id = TrackingTypeRepo.getidbyname(self.subscriptiontype, item.infos.tracking_type)
            )
            datalist.append(subscription)

        return self.subscriptiontype.create(data=datalist)

    # update subscription type function
    async def update(self, code: int, tokendata:dict, data: CreateSubscriptionType) -> SubscriptionTypeModel:
        old_data = jsonable_encoder(self.subscriptiontype.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription Type not found",
            )

        if (hasattr(data.infos, "supply_mode") and data.infos.supply_mode is not None):
            data.supply_mode_id = SupplyModeRepo.getidbyname(self.subscriptiontype, data.infos.supply_mode)
            
        if (hasattr(data.infos, "tracking_type") and data.infos.tracking_type is not None):
            data.tracking_type_id = TrackingTypeRepo.getidbyname(self.subscriptiontype, data.infos.tracking_type)

        current_data = jsonable_encoder(self.subscriptiontype.update(code, data=data.dict()))
        logs = [await Helper.build_log(f"/subscriptiontypes/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # delete subscription type %function
    async def delete(self, code: int) -> None:
        data = self.subscriptiontype.getbycode(code=code)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription Type not found",
            )

        self.subscriptiontype.delete(data)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Subscription Type deleted",
        )
