from typing import List
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from api.salesfinancial.models.SubscriptionLevelModel import SubscriptionLevelModel
from api.salesfinancial.schemas.SubscriptionLevelSchema import CreateSubscriptionLevel
from api.salesfinancial.repositories.SubscriptionLevelRepo import SubscriptionLevelRepo


class SubscriptionLevelService:
    invoicelevel: SubscriptionLevelRepo

    def __init__(
        self,
        invoicelevel: SubscriptionLevelRepo = Depends(),
    ) -> None:
        self.invoicelevel = invoicelevel

    # get all invoice levels function
    async def list(self, skip: int = 0, limit: int = 100) -> List[SubscriptionLevelModel]:
        return self.invoicelevel.list(
            skip=skip, limit=limit
        )

    # get invoice level by id function
    async def get(self, id: int) -> SubscriptionLevelModel:
        return self.invoicelevel.get(id=id)

    # get invoice level by code function
    async def getbycode(self, code: str) -> SubscriptionLevelModel:
        return self.invoicelevel.getbycode(code=code)

    # get invoice level by name function
    async def getbyname(self, name: str) -> SubscriptionLevelModel:
        return self.invoicelevel.getbyname(name=name)

    # create invoice level function
    async def create(self, data: List[CreateSubscriptionLevel]) -> List[CreateSubscriptionLevel]:
        for item in data:
            invoicelevel = self.invoicelevel.getbycode(code=item.code)
            if invoicelevel:
                raise HTTPException(
                    level_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Subscription Level already registered with code {item.code}"
                )

            invoicelevel = self.invoicelevel.getbyname(name=item.name)
            if invoicelevel:
                raise HTTPException(
                    level_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Subscription Level already registered with name {item.name}"
                )

        return self.invoicelevel.create(data=data)

    # update invoice level function
    async def update(self, code: int, data: CreateSubscriptionLevel) -> SubscriptionLevelModel:
        old_data = jsonable_encoder(self.subscriptionstatus.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription Status not found",
            )

        current_data = jsonable_encoder(self.subscriptionstatus.update(code, data=data.dict()))
        logs = [Helper.build_log(f"/subscriptionstatus/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # delete invoice level %function
    async def delete(self, code: int) -> None:
        data = self.invoicelevel.getbycode(code=code)
        if data is None:
            raise HTTPException(
                level_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription Level not found",
            )

        self.invoicelevel.delete(data)
        return HTTPException(
            level_code=status.HTTP_200_OK,
            detail="Subscription Level deleted",
        )
