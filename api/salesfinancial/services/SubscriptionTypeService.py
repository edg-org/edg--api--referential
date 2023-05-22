from typing import List
from fastapi import Depends, HTTPException, status
from api.salesfinancial.models.SubscriptionTypeModel import SubscriptionTypeModel
from api.salesfinancial.repositories.SubscriptionTypeRepo import SubscriptionTypeRepo
from api.salesfinancial.schemas.SubscriptionTypeSchema import SubscriptionTypeInput, CreateSubscriptionType

from api.salesfinancial.repositories.TrackingTypeRepo import (
    TrackingTypeRepo,
)
from api.electrical.repositories.SupplyModeRepo import (
    SupplyModeRepo,
)

class SubscriptionTypeService:
    subscriptiontype: SubscriptionTypeRepo

    def __init__(
        self,
        subscriptiontype: SubscriptionTypeRepo = Depends(),
    ) -> None:
        self.subscriptiontype = subscriptiontype

    # get all subscription types function
    async def list(self, skip: int = 0, limit: int = 100) -> List[SubscriptionTypeModel]:
        return self.subscriptiontype.list(
            skip=skip, limit=limit
        )

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
                    detail="Subscription Type already registered with code "
                    + str(item.code),
                )

            subscriptiontype = self.subscriptiontype.getbyname(name=item.name)

            if subscriptiontype:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Subscription Type already registered with name "
                    + item.name,
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
    async def update(self, code: int, data: CreateSubscriptionType) -> SubscriptionTypeModel:
        subscriptiontype = self.subscriptiontype.getbycode(code=code)
        if subscriptiontype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription Type not found",
            )
            
        subscription = CreateSubscriptionType(
            code = data.code,
            name = data.name,
            infos = data.infos,
            pricing = data.pricing,
            dunning = data.dunning,
            supply_mode_id = SupplyModeRepo.getidbyname(self.subscriptiontype, data.infos.supply_mode),
            tracking_type_id = TrackingTypeRepo.getidbyname(self.subscriptiontype, data.infos.tracking_type)
        )
        typedict = subscription.dict(exclude_unset=True)
        for key, val in typedict.items():
            setattr(subscriptiontype, key, val)
        return self.subscriptiontype.update(subscriptiontype)

    # delete subscription type %function
    async def delete(self, subscription: SubscriptionTypeModel) -> None:
        subscriptiontype = self.subscriptiontype.getbycode(code=code)
        if subscriptiontype is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription Type not found",
            )

        self.subscriptiontype.update(subscription)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Subscription Type deleted",
        )
