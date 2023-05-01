from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.configs.Environment import get_environment_variables
from api.metadata.Tags import Tags
from api.models.BaseModel import init
from api.routers.v1.LogsRouter import LogsRouter
from api.routers.v1.RefMicroServicesRouter import RefMicroServicesRouter
from api.routers.v1.RefRegionalDelegationsRouter import RefRegionalDelegationsRouter
from api.routers.v1.RefNaturalRegionsRouter import RefNaturalRegionsRouter
from api.routers.v1.RefCityTypesRouter import RefCityTypesRouter
from api.routers.v1.RefCityLevelsRouter import RefCityLevelsRouter
from api.routers.v1.RefPrefecturesRouter import RefPrefecturesRouter
from api.routers.v1.RefAdmRegionsRouter import RefAdmRegionsRouter
from api.routers.v1.RefCitiesRouter import RefCitiesRouter
from api.routers.v1.RefAreasRouter import RefAreasRouter
from api.routers.v1.RefAgenciesRouter import RefAgenciesRouter
from api.routers.v1.RefTypeAreasRouter import RefTypeAreasRouter

# Application Environment Configuration 
env = get_environment_variables()

origins = ["http://localhost:3000", "*",]

# Core Application Instance 
app = FastAPI(
    title="EDG référentiel géographique API",
    # title=env.APP_NAME,
    version=env.API_VERSION,
    openapi_tags=Tags,
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Add Routers
app.include_router(RefTypeAreasRouter)
app.include_router(RefAgenciesRouter)
app.include_router(RefAreasRouter)
app.include_router(RefCitiesRouter)
app.include_router(RefCityLevelsRouter)
app.include_router(RefCityTypesRouter)
app.include_router(RefPrefecturesRouter)
app.include_router(RefAdmRegionsRouter)
app.include_router(RefNaturalRegionsRouter)
# app.include_router(RefRegionalDelegationsRouter)
app.include_router(RefMicroServicesRouter)
app.include_router(LogsRouter)

# Initialise Data Model Attributes
init()