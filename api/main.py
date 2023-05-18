from fastapi import FastAPI

from api.metadata.Tags import Tags
from api.configs.BaseModel import init
from api.configs.Environment import get_env_var

from api.salesfinancial.routers.v1.ContactType import contacttypeRouter
from api.salesfinancial.routers.v1.TrackingType import trackingtypeRouter
from api.salesfinancial.routers.v1.InvoiceStatus import invoicestatusRouter
from api.salesfinancial.routers.v1.PricingHistory import pricinghistoryRouter
from api.salesfinancial.routers.v1.SubscriptionType import subscriptiontypeRouter
from api.salesfinancial.routers.v1.SubscriptionLevel import subscriptionlevelRouter
from api.salesfinancial.routers.v1.InvoicingFrequency import invoicingfrequencyRouter
from api.salesfinancial.routers.v1.SubscriptionStatus import subscriptionstatusRouter

from api.ageographical.routers.v1.Area import areaRouter
from api.ageographical.routers.v1.City import cityRouter
from api.ageographical.routers.v1.Agency import agencyRouter
from api.ageographical.routers.v1.Region import regionRouter
from api.ageographical.routers.v1.NaturalZone import zoneRouter
from api.ageographical.routers.v1.AreaType import areatypeRouter
from api.ageographical.routers.v1.CityType import citytypeRouter
from api.ageographical.routers.v1.CityLevel import citylevelRouter
from api.ageographical.routers.v1.Prefecture import prefectureRouter
from api.ageographical.routers.v1.DeliveryPoint import deliverypointRouter

from api.electrical.routers.v1.SupplyMode import supplymodeRouter
from api.electrical.routers.v1.ElectricMeter import meterRouter
from api.electrical.routers.v1.MeterType import metertypeRouter

from api.electrical.routers.v1.Transformer import transformerRouter
from api.electrical.routers.v1.SupplyLineType import linetypeRouter
from api.electrical.routers.v1.EnergySupplyLine import energysupplyRouter
from api.electrical.routers.v1.ConnectionPoint import connectionpointRouter

from api.electrical.routers.v1.MeterDeliveryPoint import meterdeliveryRouter

from api.loggers.routers.v1.Logger import loggerRouter

# Application Environment Configuration
env = get_env_var()

# Core Application Instance
app = FastAPI(
    title=env.app_name,
    description=env.app_desc,
    version="0.0." + env.api_version,
    openapi_tags=Tags,
)

# Add Routers
app.include_router(contacttypeRouter)
app.include_router(trackingtypeRouter)
app.include_router(invoicestatusRouter)
app.include_router(pricinghistoryRouter)
app.include_router(subscriptiontypeRouter)
app.include_router(subscriptionlevelRouter)
app.include_router(invoicingfrequencyRouter)
app.include_router(subscriptionstatusRouter)

app.include_router(zoneRouter)
app.include_router(regionRouter)
app.include_router(prefectureRouter)
app.include_router(citytypeRouter)
app.include_router(citylevelRouter)
app.include_router(areatypeRouter)
app.include_router(cityRouter)
app.include_router(agencyRouter)
app.include_router(areaRouter)
app.include_router(deliverypointRouter)


app.include_router(supplymodeRouter)
app.include_router(metertypeRouter)
app.include_router(meterRouter)
app.include_router(meterdeliveryRouter)

app.include_router(linetypeRouter)
app.include_router(transformerRouter)
app.include_router(energysupplyRouter)
app.include_router(connectionpointRouter)

app.include_router(loggerRouter)

# Initialize Data Model
init()
