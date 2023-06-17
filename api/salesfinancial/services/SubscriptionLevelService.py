from typing import List
from fastapi import Depends, HTTPException, status
from api.salesfinancial.models.SubscriptionLevelModel import SubscriptionLevelModel
from api.salesfinancial.schemas.SubscriptionLevelSchema import CreateSubscriptionLevel
from api.salesfinancial.repositories.SubscriptionLevelRepo import SubscriptionLevelRepo
from fastapi.encoders import jsonable_encoder
from api.tools.Helper import build_log
from api.logs.repositories.LogRepo import LogRepo

class SubscriptionLevelService:
    subscriptionlevels: SubscriptionLevelRepo
    log: LogRepo
    def __init__(
        self,
        subscriptionlevels: SubscriptionLevelRepo = Depends(), log: LogRepo = Depends(),
    ) -> None:
        self.subscriptionlevels = subscriptionlevels
        self.log = log

    # get all invoice levels function
    async def list(self, skip: int = 0, limit: int = 100) -> List[SubscriptionLevelModel]:
        return self.subscriptionlevels.list(
            skip=skip, limit=limit
        )

    # get invoice level by id function
    async def get(self, id: int) -> SubscriptionLevelModel:
        return self.subscriptionlevels.get(id=id)

    # get invoice level by code function
    async def getbycode(self, code: str) -> SubscriptionLevelModel:
        return self.subscriptionlevels.getbycode(code=code)

    # get invoice level by name function
    async def getbyname(self, name: str) -> SubscriptionLevelModel:
        return self.subscriptionlevels.getbyname(name=name)

    # create invoice level function
    async def create(self, data: List[CreateSubscriptionLevel]) -> List[CreateSubscriptionLevel]:
        for item in data:
            subscriptionlevels = self.subscriptionlevels.getbycode(code=item.code)
            if subscriptionlevels:
                raise HTTPException(
                    level_code=status.HTTP_400_BAD_REQUEST,
                    detail="Subscription Level already registered with code "
                    + str(item.code),
                )

            subscriptionlevels = self.subscriptionlevels.getbyname(name=item.name)
            if subscriptionlevels:
                raise HTTPException(
                    level_code=status.HTTP_400_BAD_REQUEST,
                    detail="Subscription Level already registered with name "
                    + item.name,
                )

        return self.subscriptionlevels.create(data=data)

    async def update(self, code: int, data: CreateSubscriptionLevel) -> SubscriptionLevelModel:
        old_data = jsonable_encoder(self.subscriptionlevels.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription Level not found",
            )

        verif = self.subscriptionlevels.verif_duplicate(data.name, "SubscriptionLevelModel.id != " + str(old_data['id']))
        if len(verif) != 0:
            raise HTTPException(status_code=405, detail={"msg": "Duplicates are not possible", "name": data.name})

        current_data = jsonable_encoder(self.subscriptionlevels.update(code=code, data=data.dict()))
        logs = [await build_log(f"/subscriptionlevels/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        self.log.create(logs)
        return current_data

    # delete invoice level %function
    async def delete(self, invoice: SubscriptionLevelModel) -> None:
        code = 0
        subscriptionlevels = self.subscriptionlevels.getbycode(code=code)
        if subscriptionlevels is None:
            raise HTTPException(
                level_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription Level not found",
            )

        self.subscriptionlevels.update(invoice)
        return HTTPException(
            level_code=status.HTTP_200_OK,
            detail="Subscription Level deleted",
        )
