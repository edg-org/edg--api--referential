from typing import List
from fastapi import Depends, HTTPException, status
from api.salesfinancial.models.PricingHistoryModel import PricingHistoryModel
from api.salesfinancial.repositories.PricingHistoryRepo import PricingHistoryRepo
from api.salesfinancial.schemas.PricingHistorySchema import CreatePricingHistory

class PricingHistoryService:
    pricinghistory: PricingHistoryRepo

    def __init__(
        self, pricinghistory: PricingHistoryRepo = Depends()
    ) -> None:
        self.pricinghistory = pricinghistory

    # get all pricing histories function
    async def list(self, skip: int = 0, limit: int = 100) -> List[PricingHistoryModel]:
        return self.pricinghistory.list(
            skip=skip, limit=limit
        )

    # get pricing history by id function
    async def get(self, id: int) -> PricingHistoryModel:
        return self.pricinghistory.get(id=id)

    # get pricing history by code function
    async def getbycode(self, code: str) -> PricingHistoryModel:
        return self.pricinghistory.getbycode(code=code)

    # get pricing history by name function
    async def getbyname(self, name: str) -> PricingHistoryModel:
        return self.pricinghistory.getbyname(name=name)

    # create pricing history function
    async def create(self, data: List[CreatePricingHistory]) -> List[CreatePricingHistory]:
        for item in data:
            pricinghistory = self.pricinghistory.getbycode(
                code=item.code
            )
            if pricinghistory:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Pricing History already registered with code "
                    + str(item.code),
                )

            pricinghistory = self.pricinghistory.getbyname(
                name=item.name
            )
            if pricinghistory:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Pricing History already registered with name "
                    + item.name,
                )

        return self.pricinghistory.create(data=data)