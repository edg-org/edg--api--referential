from typing import List
from api.configs.Environment import get_env_var
from fastapi import APIRouter, Depends, status, HTTPException
from api.loggers.services.LoggerService import LoggerService
from api.loggers.schemas.LoggerSchema import (
    LoggerInput,
    LoggerSchema,
    CreateLogger
)

env = get_env_var()
router_path = env.api_routers_prefix+env.api_version

loggerRouter = APIRouter(
    prefix=router_path+"/loggers",
    tags=["Loggers"]
)

#get all cities route
@loggerRouter.get(
    "/",
    summary="Getting router for all logs",
    description="This router allows to get all logs",
    response_model=List[LoggerSchema]
)
async def list(skip: int=0, limit: int=100, logService: LoggerService = Depends()):
    return await logService.list(skip=skip, limit=limit)

#get city route
@loggerRouter.get(
    "/{id}",
    summary="Getting router a city without items",
    description="This router allows to get a log",
    response_model=LoggerSchema
)
async def get(id: int, logService: LoggerService = Depends()):
    log = await logService.get(id=id)
    if log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="logs not found")
    return log

#post area type route
@loggerRouter.post(
    "/",
    summary="Creation router a log",
    description="This router allows to create a log",
    response_model=List[CreateLogger]
)
async def create(
    data: List[LoggerInput], 
    loggerService: LoggerService = Depends()
):
    return await loggerService.create(data=data)