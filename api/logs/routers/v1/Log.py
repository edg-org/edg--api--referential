from typing import List
from api.tools.JWTBearer import JWTBearer, env
from api.logs.services.LogService import LogService
from fastapi import (
    status, 
    Depends, 
    APIRouter, 
    HTTPException
)
from api.logs.schemas.LogSchema import (
    LogInput,
    LogSchema,
    CreateLog
)

router_path = env.api_routers_prefix+env.api_version

logRouter = APIRouter(
    tags=["Logs"],
    prefix=router_path+"/logs",
    dependencies=[Depends(JWTBearer())]
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