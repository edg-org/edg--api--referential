from typing import List, Optional

from fastapi import Depends
from api.models.LogsModel import Logs

from api.repositories.LogsRepository import LogsRepository
from api.schemas.pydantic.LogsSchema import LogsSchema,LogsCreateSchema,LogsUpdateSchema


class LogsService:
    logs: LogsRepository
    def __init__(self, logs: LogsRepository = Depends()) -> None:
        self.logs = logs

    def create(self, log_body: LogsCreateSchema):
    # def create(self, log_body: LogsCreateSchema) -> LogsSchema:
        return self.logs.create(log_body)

    def get(self, id: int) -> Logs:
        return self.logs.get(id)

    def list(self, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[Logs]:
        return self.logs.list(skip, limit)

    def update(self, log_body: LogsUpdateSchema) -> Logs:
        ref_log = self.logs.get(log_body.id)
        return self.logs.update(log_body)

    # def delete(self, id: int) -> Logs:
    def delete(self, id: int):
        ref_log = self.logs.get(id, True)
        return self.logs.delete(id)

    def retaure(self, id: int):
        ref_log = self.logs.get(id, False)
        return self.logs.delete(id, True)

    def delete_signature(self, id : int, signature : str):
        ref_log = self.logs.get_id_and_signature(id, signature)
        return self.logs.delete_signature(id, signature)

    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None) :
        return self.logs.get_items(id, code, signature)






