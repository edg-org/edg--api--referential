from typing import List
from fastapi import Depends, HTTPException, status
from api.sales_financial.models.SubscriptionTypeModel import SubscriptionTypeModel
from api.sales_financial.repositories.SubscriptionTypeRepo import SubscriptionTypeRepo
from api.sales_financial.schemas.SubscriptionTypeSchema import SubscriptionTypeBase, CreateSubscriptionType

class SubscriptionTypeService:
    subscriptiontype: SubscriptionTypeRepo

    def __init__(
        self, subscriptiontype: SubscriptionTypeRepo = Depends()
    ) -> None:
        self.subscriptiontype = subscriptiontype

    # get all subscription types function
    async def list(self, skip: int = 0, limit: int = 100) -> List[SubscriptionTypeModel]:
        return self.subscriptiontype.list(skip=skip, limit=limit)

    # get subscription type by id function
    async def get(self, id: int) -> SubscriptionTypeModel:
        return self.subscriptiontype.get(id=id)
    
    # get subscription type by code function
    async def getbycode(self, code: str) -> SubscriptionTypeBase:
        return self.subscriptiontype.getbycode(code=code)
    
    # get subscription type by name function
    async def getbyname(self, name: str) -> SubscriptionTypeBase:
        return self.subscriptiontype.getbyname(name=name)

    # create subscription type function
    async def create(self, data: List[CreateSubscriptionType]) -> List[CreateSubscriptionType]:
        for item in data:
            subscriptiontype = self.subscriptiontype.getbycode(code=item.code)
            if subscriptiontype:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Subscription Type already registered with code "+ str(item.code))
            
            subscriptiontype = self.subscriptiontype.getbyname(name=item.name)
            if subscriptiontype:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Subscription Type already registered with name "+ item.name)
        
        return self.subscriptiontype.create(data=data)

    # update subscription type function
    async def update(self, code: int, data: SubscriptionTypeBase) -> SubscriptionTypeModel:
        subscriptiontype = self.subscriptiontype.get(code=code)
        if subscriptiontype is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription Type not found")
        
        typedict = data.dict(exclude_unset=True)
        for key, val in typedict.items():
            setattr(subscriptiontype, key, val)
        return self.subscriptiontype.update(subscriptiontype)

    # delete subscription type %function
    async def delete(self, subscription: SubscriptionTypeModel) -> None:
        subscriptiontype = self.subscriptiontype.get(id=id)
        if subscriptiontype is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription Type not found")
        
        self.subscriptiontype.update(subscription)
        return HTTPException(status_code=status.HTTP_200_OK, detail="Subscription Type deleted")