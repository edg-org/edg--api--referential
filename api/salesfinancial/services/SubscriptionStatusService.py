from typing import List
from fastapi import Depends, HTTPException, status
from api.salesfinancial.models.SubscriptionStatusModel import SubscriptionStatusModel
from api.salesfinancial.schemas.SubscriptionStatusSchema import CreateSubscriptionStatus
from api.salesfinancial.repositories.SubscriptionStatusRepo import SubscriptionStatusRepo
from fastapi.encoders import jsonable_encoder
from api.tools.Helper import build_log
from api.logs.repositories.LogRepo import LogRepo

class SubscriptionStatusService:
    subscriptionstatus: SubscriptionStatusRepo
    log: LogRepo
    def __init__(
        self,
        subscriptionstatus: SubscriptionStatusRepo = Depends(), log: LogRepo = Depends(),
    ) -> None:
        self.subscriptionstatus = subscriptionstatus
        self.log = log
    # get all subscription status function
    async def list(self, skip: int = 0, limit: int = 100) -> List[SubscriptionStatusModel]:
        return self.subscriptionstatus.list(
            skip=skip, limit=limit
        )

    # get subscription status by id function
    async def get(self, id: int) -> SubscriptionStatusModel:
        return self.subscriptionstatus.get(id=id)

    # get subscription status by code function
    async def getbycode(self, code: str) -> SubscriptionStatusModel:
        return self.subscriptionstatus.getbycode(code=code)

    # get subscription status by name function
    async def getbyname(self, name: str) -> SubscriptionStatusModel:
        return self.subscriptionstatus.getbyname(name=name)

    # create subscription status function
    async def create(self, data: List[CreateSubscriptionStatus]) -> List[CreateSubscriptionStatus]:
        for item in data:
            subscriptionstatus = self.subscriptionstatus.getbycode(code=item.code)
            
            if subscriptionstatus:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Subscription Status already registered with code "
                    + str(item.code),
                )

            subscriptionstatus = self.subscriptionstatus.getbyname(name=item.name)
            
            if subscriptionstatus:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Subscription Status already registered with name "
                    + item.name,
                )

        return self.subscriptionstatus.create(data=data)

    # update subscription status function
    # async def update(self, code: int, data: CreateSubscriptionStatus) -> SubscriptionStatusModel:
    #     subscriptionstatus = self.subscriptionstatus.getbycode(code=code)
    #     if subscriptionstatus is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail="Subscription Status not found",
    #         )
    #
    #     statusdict = data.dict(exclude_unset=True)
    #     for key, val in statusdict.items():
    #         setattr(subscriptionstatus, key, val)
    #     return self.subscriptionstatus.update(subscriptionstatus)

    async def update(self, code: int, data: CreateSubscriptionStatus) -> SubscriptionStatusModel:
        old_data = jsonable_encoder(self.subscriptionstatus.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact Type not found",
            )

        verif = self.subscriptionstatus.verif_duplicate(data.name, "SubscriptionStatusModel.id != " + str(old_data['id']))
        if len(verif) != 0:
            raise HTTPException(status_code=405, detail={"msg": "Duplicates are not possible", "name": data.name})

        current_data = jsonable_encoder(self.subscriptionstatus.update(code=code, data=data.dict()))
        logs = [await build_log(f"/subscriptionstatus/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        self.log.create(logs)
        return current_data

    # delete subscription status %function
    async def delete(self, subscription: SubscriptionStatusModel) -> None:
        code = "" #
        subscriptionstatus = self.subscriptionstatus.getbycode(code=code)
        if subscriptionstatus is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription Status not found",
            )

        self.subscriptionstatus.update(subscription)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Subscription Status deleted",
        )
