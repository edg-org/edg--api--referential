from typing import List
from fastapi import Depends, HTTPException, status
from api.sales_financial.models.SubscriptionLevelModel import SubscriptionLevelModel
from api.sales_financial.repositories.SubscriptionLevelRepo import SubscriptionLevelRepo
from api.sales_financial.schemas.SubscriptionLevelSchema import SubscriptionLevelBase, CreateSubscriptionLevel

class SubscriptionLevelService:
    invoicelevel: SubscriptionLevelRepo

    def __init__(
        self, invoicelevel: SubscriptionLevelRepo = Depends()
    ) -> None:
        self.invoicelevel = invoicelevel

    # get all invoice levels function
    async def list(self, skip: int = 0, limit: int = 100) -> List[SubscriptionLevelModel]:
        return self.invoicelevel.list(skip=skip, limit=limit)

    # get invoice level by id function
    async def get(self, id: int) -> SubscriptionLevelModel:
        return self.invoicelevel.get(id=id)
    
    # get invoice level by code function
    async def getbycode(self, code: str) -> SubscriptionLevelBase:
        return self.invoicelevel.getbycode(code=code)
    
    # get invoice level by name function
    async def getbyname(self, name: str) -> SubscriptionLevelBase:
        return self.invoicelevel.getbyname(name=name)

    # create invoice level function
    async def create(self, data: List[CreateSubscriptionLevel]) -> List[CreateSubscriptionLevel]:
        for item in data:
            invoicelevel = self.invoicelevel.getbycode(code=item.code)
            if invoicelevel:
                raise HTTPException(level_code=status.HTTP_400_BAD_REQUEST, detail="Subscription Level already registered with code "+ str(item.code))
            
            invoicelevel = self.invoicelevel.getbyname(name=item.name)
            if invoicelevel:
                raise HTTPException(level_code=status.HTTP_400_BAD_REQUEST, detail="Subscription Level already registered with name "+ item.name)
        
        return self.invoicelevel.create(data=data)

    # update invoice level function
    async def update(self, code: int, data: SubscriptionLevelBase) -> SubscriptionLevelModel:
        invoicelevel = self.invoicelevel.get(code=code)
        if invoicelevel is None:
            raise HTTPException(level_code=status.HTTP_404_NOT_FOUND, detail="Subscription Level not found")
        
        leveldict = data.dict(exclude_unset=True)
        for key, val in leveldict.items():
            setattr(invoicelevel, key, val)
        return self.invoicelevel.update(invoicelevel)

    # delete invoice level %function
    async def delete(self, invoice: SubscriptionLevelModel) -> None:
        invoicelevel = self.invoicelevel.get(id=id)
        if invoicelevel is None:
            raise HTTPException(level_code=status.HTTP_404_NOT_FOUND, detail="Subscription Level not found")
        
        self.invoicelevel.update(invoice)
        return HTTPException(level_code=status.HTTP_200_OK, detail="Subscription Level deleted")