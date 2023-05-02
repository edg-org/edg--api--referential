from fastapi import FastAPI

from api.metadata.Tags import Tags
from api.configs.BaseModel import init
from api.configs.Environment import get_env_var
from api.geographical.routers.v1.Area import areaRouter
from api.geographical.routers.v1.City import cityRouter
from api.geographical.routers.v1.Agency import agencyRouter
from api.geographical.routers.v1.Region import regionRouter

from api.sales.routers.v1.ContactType import contacttypeRouter
from api.sales.routers.v1.TrackingType import trackingtypeRouter
from api.sales.routers.v1.InvoiceStatus import invoicestatusRouter
from api.sales.routers.v1.PricingHistory import pricinghistoryRouter
from api.sales.routers.v1.SubscriptionType import subscriptiontypeRouter
from api.sales.routers.v1.SubscriptionLevel import subscriptionlevelRouter
from api.sales.routers.v1.InvoicingFrequency import invoicingfrequencyRouter
from api.sales.routers.v1.SubscriptionStatus import subscriptionstatusRouter

from api.geographical.routers.v1.NaturalZone import zoneRouter
from api.geographical.routers.v1.AreaType import areatypeRouter
from api.geographical.routers.v1.CityType import citytypeRouter
from api.geographical.routers.v1.CityLevel import citylevelRouter
from api.geographical.routers.v1.Prefecture import prefectureRouter

# Application Environment Configuration
env = get_env_var()

# Core Application Instance
app = FastAPI(
    title=env.app_name,
    description=env.app_desc,
    version="0.0."+env.api_version,
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
app.include_router(areaRouter)
app.include_router(agencyRouter)

# Initialize Data Model
init()