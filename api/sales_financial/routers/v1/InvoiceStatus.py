from typing import List
from api.configs.Environment import get_env_var
from fastapi import Depends, APIRouter, status, HTTPException
from api.sales_financial.services.InvoiceStatusService import InvoiceStatusService
from api.sales_financial.schemas.InvoiceStatusSchema import (
    InvoiceStatusBase, 
    CreateInvoiceStatus,
    InvoiceStatusSchema
)

env = get_env_var()
router_path = env.api_routers_prefix+env.api_version

invoicestatusRouter = APIRouter(
    prefix=router_path+"/invoicestatus",
    tags=["Invoice Status"]
)

#get all invoice status route
@invoicestatusRouter.get(
    "/",
    summary="Getting router for all invoice status",
    description="This router allows to get all invoice status",
    response_model=List[InvoiceStatusSchema]
)
async def list(skip: int=0, limit: int=100, statusService: InvoiceStatusService = Depends()):
    return await statusService.list(skip, limit)

#get invoice status route
@invoicestatusRouter.get(
    "/{code}",
    summary="Getting router a invoice status without items",
    description="This router allows to get a invoice status without items",
    response_model=InvoiceStatusSchema
)
async def get(code: int, statusService: InvoiceStatusService = Depends()):
    invoicestatus = await statusService.getbycode(code=code)
    if invoicestatus is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice Status not found")
    return invoicestatus

#post invoice status route
@invoicestatusRouter.post(
    "/",
    summary="Creation router a invoice status",
    description="This router allows to create a invoice status",
    response_model=List[CreateInvoiceStatus]
)
async def create(data: List[CreateInvoiceStatus], statusService: InvoiceStatusService = Depends()):
    return await statusService.create(data=data)

#update invoice status route
@invoicestatusRouter.put(
    "/{code}",
    summary="Update router a invoice status",
    description="This router allows to update a invoice status",
    response_model=InvoiceStatusSchema
)
async def update(code: int, data: InvoiceStatusBase, statusService: InvoiceStatusService = Depends()):
    return await statusService.update(code=code, data=data)