from typing import List
from fastapi import Depends, HTTPException, status
from api.salesfinancial.models.InvoicingFrequencyModel import InvoicingFrequencyModel
from api.salesfinancial.repositories.InvoicingFrequencyRepo import InvoicingFrequencyRepo
from api.salesfinancial.schemas.InvoicingFrequencySchema import CreateInvoicingFrequency

class InvoicingFrequencyService:
    invoicingfrequency: InvoicingFrequencyRepo

    def __init__(
        self,
        invoicingfrequency: InvoicingFrequencyRepo = Depends(),
    ) -> None:
        self.invoicingfrequency = invoicingfrequency

    # get all invoicing frequencies function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[InvoicingFrequencyModel]:
        return self.invoicingfrequency.list(
            skip=skip, limit=limit
        )

    # get invoicing frequency by id function
    async def get(self, id: int) -> InvoicingFrequencyModel:
        return self.invoicingfrequency.get(id=id)

    # get invoicing frequency by code function
    async def getbycode(self, code: str) -> InvoicingFrequencyModel:
        return self.invoicingfrequency.getbycode(code=code)

    # get invoicing frequency by name function
    async def getbyname(self, name: str) -> InvoicingFrequencyModel:
        return self.invoicingfrequency.getbyname(name=name)
    
    # get invoicing frequency by shortname function
    async def getbyname(self, shortname: str) -> InvoicingFrequencyModel:
        return self.invoicingfrequency.getbyshortname(shortname=shortname)

    # create invoicing frequency function
    async def create(self, data: List[CreateInvoicingFrequency]) -> List[CreateInvoicingFrequency]:
        for item in data:
            invoicingfrequency = self.invoicingfrequency.getbycode(code=item.code)
            if invoicingfrequency:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invoicing Frequency already registered with code "
                    + str(item.code),
                )

            invoicingfrequency = self.invoicingfrequency.getbyname(name=item.name)
            if invoicingfrequency:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invoicing Frequency already registered with name "
                    + item.name,
                )

        return self.invoicingfrequency.create(data=data)

    # update invoicing frequency function
    async def update(self, code: int, data: CreateInvoicingFrequency) -> InvoicingFrequencyModel:
        invoicingfrequency = self.invoicingfrequency.getbycode(code=code)
        if invoicingfrequency is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoicing Frequency not found",
            )

        frequencydict = data.dict(exclude_unset=True)
        for key, val in frequencydict.items():
            setattr(invoicingfrequency, key, val)
        return self.invoicingfrequency.update(
            invoicingfrequency
        )

    # delete invoicing frequency %function
    async def delete(self, invoicing: InvoicingFrequencyModel) -> None:
        invoicingfrequency = self.invoicingfrequency.getbycode(code=code)
        if invoicingfrequency is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoicing Frequency not found",
            )

        self.invoicingfrequency.update(invoicing)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Invoicing Frequency deleted",
        )