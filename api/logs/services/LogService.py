from typing import List, Optional

from fastapi import Depends
from api.logs.models.LogModel import LogModel
from api.logs.schemas.LogSchema import CreateLog
from api.logs.repositories.LogRepo import LogRepo


class LogService:
    logs: LogRepo
    
    def __init__(self, logs: LogRepo = Depends()) -> None:
        self.logs = logs

    # get all logs
    async def list(self, skip: int = 0, limit: int = 100) -> List[LogModel]:
        return self.logs.list(skip=skip, limit=limit)
    
    # get log by id
    async def get(self, id: int) -> LogModel:
        return self.logs.get(id=id)

    # create logs function
    async def create(self, data: List[CreateLog]) -> List[CreateLog]:
        return self.logs.create(data=data)