from typing import List
from api.configs.Environment import get_env_var
from fastapi import (
    Depends,
    APIRouter,
    status,
    HTTPException,
)
from api.salesfinancial.services.InvoicingFrequencyService import (
    InvoicingFrequencyService,
)
from api.salesfinancial.schemas.InvoicingFrequencySchema import (
    InvoicingFrequencyBase,
    CreateInvoicingFrequency,
    InvoicingFrequencyUpdate,
    InvoicingFrequencySchema
)

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

invoicingfrequencyRouter = APIRouter(
    prefix=router_path + "/invoicingfrequencies",
    tags=["Invoicing Frequencies"],
)


# get all invoicing frequency route
@invoicingfrequencyRouter.get(
    "/",
    summary="Getting router for all invoicing frequencies",
    description="This router allows to get all invoicing frequencies",
    response_model=List[InvoicingFrequencySchema],
)
async def list(
    skip: int = 0,
    limit: int = 100,
    frequencyService: InvoicingFrequencyService = Depends(),
):
    return await frequencyService.list(skip, limit)


# get invoicing frequency route
@invoicingfrequencyRouter.get(
    "/{code}",
    summary="Getting router a invoicing frequency without items",
    description="This router allows to get a invoicing frequency without items",
    response_model=InvoicingFrequencySchema,
)
async def get(
    code: int,
    frequencyService: InvoicingFrequencyService = Depends(),
):
    invoicingfrequency = await frequencyService.getbycode(
        code=code
    )
    if invoicingfrequency is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoicing Frequency not found",
        )
    return invoicingfrequency


# post invoicing frequency route
@invoicingfrequencyRouter.post(
    "/",
    summary="Creation router a invoicing frequency",
    description="This router allows to create a invoicing frequency",
    response_model=List[CreateInvoicingFrequency],
)
async def create(
    data: List[CreateInvoicingFrequency],
    frequencyService: InvoicingFrequencyService = Depends(),
):
    return await frequencyService.create(data=data)


# update invoicing frequency route
@invoicingfrequencyRouter.put(
    "/{code}",
    summary="Update router a invoicing frequency",
    description="This router allows to update a invoicing frequency",
    response_model=InvoicingFrequencySchema,
)
async def update(
    code: int,
    data: InvoicingFrequencyUpdate,
    frequencyService: InvoicingFrequencyService = Depends(),
):
    return await frequencyService.update(
        code=code, data=data
    )
