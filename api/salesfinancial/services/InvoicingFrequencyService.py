from typing import List
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from api.logs.services.LogService import LogService
from api.salesfinancial.models.InvoicingFrequencyModel import InvoicingFrequencyModel
from api.salesfinancial.repositories.InvoicingFrequencyRepo import InvoicingFrequencyRepo
from api.salesfinancial.schemas.InvoicingFrequencySchema import CreateInvoicingFrequency

class InvoicingFrequencyService:
    log: LogService
    invoicingfrequency: InvoicingFrequencyRepo

    def __init__(
        self,
        log: LogService = Depends(),
        invoicingfrequency: InvoicingFrequencyRepo = Depends()
    ) -> None:
        self.log = log
        self.invoicingfrequency = invoicingfrequency

    # get all invoicing frequencies function
    async def list(self, start: int = 0, size: int = 100) -> List[InvoicingFrequencyModel]:
        return self.invoicingfrequency.list(start=start, size=size)

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
                    detail=f"Invoicing Frequency already registered with code {item.code}"
                )

            invoicingfrequency = self.invoicingfrequency.getbyname(name=item.name)
            if invoicingfrequency:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invoicing Frequency already registered with name {item.name}"
                )

        return self.invoicingfrequency.create(data=data)

    # update invoicing frequency function
    async def update(self, code: int, tokendata: dict, data: CreateInvoicingFrequency) -> InvoicingFrequencyModel:
        old_data = jsonable_encoder(self.invoicingfrequency.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription Status not found",
            )

        current_data = jsonable_encoder(self.invoicingfrequency.update(code, data=data.dict()))
        logs = [await Helper.build_log(f"/invoicingfrequencies/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # delete invoicing frequency %function
    async def delete(self, code: int) -> None:
        data = self.invoicingfrequency.getbycode(code=code)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoicing Frequency not found"
            )

        self.invoicingfrequency.delete(data)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Invoicing Frequency deleted"
        )