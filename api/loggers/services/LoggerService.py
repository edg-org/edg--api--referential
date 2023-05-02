from typing import List, Optional

from fastapi import Depends
from api.loggers.models.LoggerModel import LoggerModel
from api.loggers.schemas.LoggerSchema import CreateLogger
from api.loggers.repositories.LoggerRepo import LoggerRepo


class LoggerService:
    logs: LoggerRepo
    
    def __init__(
        self, logs: LoggerRepo = Depends()
    ) -> None:
        self.logs = logs

    # get all logs
    async def list(self, skip: int = 0, limit: int = 100) -> List[LoggerModel]:
        return self.logs.list(skip=skip, limit=limit)
    
    # get log by id
    async def get(self, id: int) -> LoggerModel:
        return self.logs.get(id=id)

    # create logs function
    async def create(self, data: List[CreateLogger]) -> List[CreateLogger]:
        return self.logs.create(data=data)