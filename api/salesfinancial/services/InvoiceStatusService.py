from typing import List
from fastapi import Depends, HTTPException, status
from api.salesfinancial.models.InvoiceStatusModel import (
    InvoiceStatusModel,
)
from api.salesfinancial.repositories.InvoiceStatusRepo import (
    InvoiceStatusRepo,
)
from api.salesfinancial.schemas.InvoiceStatusSchema import (
    InvoiceStatusBase,
    CreateInvoiceStatus,
)


class InvoiceStatusService:
    invoicestatus: InvoiceStatusRepo

    def __init__(
        self, invoicestatus: InvoiceStatusRepo = Depends()
    ) -> None:
        self.invoicestatus = invoicestatus

    # get all invoice statuss function
    async def list(
        self, skip: int = 0, limit: int = 100
    ) -> List[InvoiceStatusModel]:
        return self.invoicestatus.list(
            skip=skip, limit=limit
        )

    # get invoice status by id function
    async def get(self, id: int) -> InvoiceStatusModel:
        return self.invoicestatus.get(id=id)

    # get invoice status by code function
    async def getbycode(
        self, code: str
    ) -> InvoiceStatusBase:
        return self.invoicestatus.getbycode(code=code)

    # get invoice status by name function
    async def getbyname(
        self, name: str
    ) -> InvoiceStatusBase:
        return self.invoicestatus.getbyname(name=name)

    # create invoice status function
    async def create(
        self, data: List[CreateInvoiceStatus]
    ) -> List[CreateInvoiceStatus]:
        for item in data:
            invoicestatus = self.invoicestatus.getbycode(
                code=item.code
            )
            if invoicestatus:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invoice Status already registered with code "
                    + str(item.code),
                )

            invoicestatus = self.invoicestatus.getbyname(
                name=item.name
            )
            if invoicestatus:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invoice Status already registered with name "
                    + item.name,
                )

        return self.invoicestatus.create(data=data)

    # update invoice status function
    async def update(
        self, code: int, data: InvoiceStatusBase
    ) -> InvoiceStatusModel:
        invoicestatus = self.invoicestatus.get(code=code)
        if invoicestatus is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice Status not found",
            )

        statusdict = data.dict(exclude_unset=True)
        for key, val in statusdict.items():
            setattr(invoicestatus, key, val)
        return self.invoicestatus.update(invoicestatus)

    # delete invoice status %function
    async def delete(
        self, invoice: InvoiceStatusModel
    ) -> None:
        invoicestatus = self.invoicestatus.get(id=id)
        if invoicestatus is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice Status not found",
            )

        self.invoicestatus.update(invoice)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Invoice Status deleted",
        )
