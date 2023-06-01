from typing import List
from api.configs.Environment import get_env_var
from fastapi import APIRouter, Depends, status, HTTPException
from api.logs.services.LogService import LogService
from api.logs.schemas.LogSchema import (
    LogInput,
    LogSchema,
    CreateLog
)

env = get_env_var()
router_path = env.api_routers_prefix+env.api_version

logRouter = APIRouter(
    prefix=router_path+"/logs",
    tags=["Logs"]
)

#get all cities route
@logRouter.get(
    "/",
    summary="Getting router for all logs",
    description="This router allows to get all logs",
    response_model=List[LogSchema]
)
async def list(skip: int=0, limit: int=100, logService: LogService = Depends()):
    return await logService.list(skip=skip, limit=limit)

#get city route
@logRouter.get(
    "/{id}",
    summary="Getting router a city without items",
    description="This router allows to get a log",
    response_model=LogSchema
)
async def get(id: int, logService: LogService = Depends()):
    log = await logService.get(id=id)
    if log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="logs not found")
    return log

#post area type route
@logRouter.post(
    "/",
    summary="Creation router a log",
    description="This router allows to create a log",
    response_model=List[CreateLog]
)
async def create(
    data: List[LogInput], 
    logService: LogService = Depends()
):
    return await logService.create(data=data)