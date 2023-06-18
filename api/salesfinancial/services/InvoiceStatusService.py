from typing import List
from api.tools.Helper import Helper
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from api.logs.services.LogService import LogService
from api.salesfinancial.models.InvoiceStatusModel import InvoiceStatusModel
from api.salesfinancial.repositories.InvoiceStatusRepo import InvoiceStatusRepo
from api.salesfinancial.schemas.InvoiceStatusSchema import CreateInvoiceStatus

class InvoiceStatusService:
    log: LogService
    invoicestatus: InvoiceStatusRepo

    def __init__(
        self, 
        log: LogService = Depends(),
        invoicestatus: InvoiceStatusRepo = Depends()
    ) -> None:
        self.log = log
        self.invoicestatus = invoicestatus

    # get all invoice statuss function
    async def list(self, start: int = 0, size: int = 100) -> List[InvoiceStatusModel]:
        return self.invoicestatus.list(start=start, size=size)

    # get invoice status by id function
    async def get(self, id: int) -> InvoiceStatusModel:
        return self.invoicestatus.get(id=id)

    # get invoice status by code function
    async def getbycode(self, code: str) -> InvoiceStatusModel:
        return self.invoicestatus.getbycode(code=code)

    # get invoice status by name function
    async def getbyname(self, name: str) -> InvoiceStatusModel:
        return self.invoicestatus.getbyname(name=name)

    # create invoice status function
    async def create(
        self, data: List[CreateInvoiceStatus]
    ) -> List[CreateInvoiceStatus]:
        for item in data:
            invoicestatus = self.invoicestatus.getbycode(code=item.code)
            if invoicestatus:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invoice Status already registered with code {item.code}"
                )

            invoicestatus = self.invoicestatus.getbyname(name=item.name)
            if invoicestatus:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invoice Status already registered with name {item.name}"
                )

        return self.invoicestatus.create(data=data)

    # update invoice status function
    async def update(self, code: int, tokendata: dict, data: CreateInvoiceStatus) -> InvoiceStatusModel:
        old_data = jsonable_encoder(self.invoicestatus.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice Status not found",
            )

        current_data = jsonable_encoder(self.invoicestatus.update(code, data=data.dict()))
        logs = [await Helper.build_log(f"/invoicestatus/{code}", "PUT", tokendata["email"], old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # delete invoice status %function
    async def delete(self, code: int) -> None:
        data = self.invoicestatus.getbycode(code=code)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice Status not found",
            )

        self.invoicestatus.delete(data)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Invoice Status deleted",
        )
