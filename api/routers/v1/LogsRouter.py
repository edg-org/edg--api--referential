from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, Query, Body, Path, Header, Cookie, Form, File

from api.schemas.pydantic.LogsSchema import (LogsSchema, LogsCreateSchema,
LogsUpdateSchema, EXAMPLE, EXAMPLE1)
from api.services.LogsService import LogsService

LogsRouter = APIRouter(prefix="/v1/logs", tags=["Logs"])

@LogsRouter.get("/", response_model=List[LogsSchema])
def index(skip: Optional[int] = 0, limit: Optional[int] = 100, logs: LogsService = Depends()):
    return jsonable_encoder(logs.list(skip,limit))

# @LogsRouter.get("/{id}")
@LogsRouter.get("/{id}", response_model=LogsSchema)
def get(id: int, logs: LogsService = Depends()):
    return logs.get(id)

@LogsRouter.post("/", response_model=LogsSchema, status_code=status.HTTP_201_CREATED)
def create(log: LogsCreateSchema = Body(example = EXAMPLE), logs: LogsService = Depends()):
    log = logs.create(log)
    return log 

@LogsRouter.put("/", response_model = LogsSchema)
# @LogsRouter.put("/")
def update(log: LogsUpdateSchema = Body(example = EXAMPLE1), logs: LogsService = Depends()):
    return logs.update(log)

@LogsRouter.delete("/{id}", response_model = LogsSchema)
# @LogsRouter.delete("/{id}")
def delete(id: int, logs: LogsService = Depends()):
    return logs.delete(id)

@LogsRouter.put("/restore/{id}", response_model = LogsSchema)
# @LogsRouter.put("/restore/{id}")
def restore(id: int, logs: LogsService = Depends()):
    return logs.retaure(id)

# @LogsRouter.delete("/{id}/{signature}")
@LogsRouter.delete("/{id}/{signature}", response_model = LogsSchema)
def delete_signature(id: int, signature: str, logs: LogsService = Depends()):
    return logs.delete_signature(id, signature)

@LogsRouter.get("/items/")
def get_items(id: Optional[int] = 0, signature: Optional[str] = None, logs: LogsService = Depends()):
# def get_items(id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, logs: LogsService = Depends()):
    return logs.get_items(id, "", signature)

