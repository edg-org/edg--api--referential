from typing import List
from fastapi import Depends, HTTPException, status
from api.salesfinancial.models.InvoiceStatusModel import InvoiceStatusModel
from api.salesfinancial.repositories.InvoiceStatusRepo import InvoiceStatusRepo
from api.salesfinancial.schemas.InvoiceStatusSchema import CreateInvoiceStatus
from fastapi.encoders import jsonable_encoder
from api.tools.Helper import build_log
from api.logs.repositories.LogRepo import LogRepo

class InvoiceStatusService:
    invoicestatus: InvoiceStatusRepo
    log: LogRepo
    def __init__(
        self, invoicestatus: InvoiceStatusRepo = Depends(), log: LogRepo = Depends()
    ) -> None:
        self.invoicestatus = invoicestatus
        self.log = log

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
                    detail="Invoice Status already registered with code "
                    + str(item.code),
                )

            invoicestatus = self.invoicestatus.getbyname(name=item.name)
            if invoicestatus:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invoice Status already registered with name "
                    + item.name,
                )

        return self.invoicestatus.create(data=data)

    # update invoice status function
    # async def update(self, code: int, data: CreateInvoiceStatus) -> InvoiceStatusModel:
    #     invoicestatus = self.invoicestatus.getbycode(code=code)
    #     if invoicestatus is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail="Invoice Status not found",
    #         )
    #
    #     statusdict = data.dict(exclude_unset=True)
    #     for key, val in statusdict.items():
    #         setattr(invoicestatus, key, val)
    #     return self.invoicestatus.update(invoicestatus)

    async def update(self, code: int, data: CreateInvoiceStatus) -> InvoiceStatusModel:
        old_data = jsonable_encoder(self.invoicestatus.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription Type not found",
            )

        verif = self.invoicestatus.verif_duplicate(data.name, "InvoiceStatusModel.id != " + str(old_data['id']))
        if len(verif) != 0:
            raise HTTPException(status_code=405, detail={"msg": "Duplicates are not possible", "name": data.name})

        current_data = jsonable_encoder(self.invoicestatus.update(code=code, data=data.dict()))
        logs = [await build_log(f"/invoicestatus/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        self.log.create(logs)
        return current_data

    # delete invoice status %function
    async def delete(self, invoice: InvoiceStatusModel) -> None:
        code = 1
        invoicestatus = self.invoicestatus.getbycode(code=code)
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
