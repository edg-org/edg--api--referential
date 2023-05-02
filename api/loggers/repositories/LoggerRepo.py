from typing import List, Optional
import json
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, lazyload
from sqlalchemy import select, insert, update, delete, and_, or_
from fastapi.encoders import jsonable_encoder
import uuid
from sqlalchemy.sql import func
from api.configs.Database import (get_db_connection,)
from api.models.LogsModel import Logs
from api.internal.Admin import add_log, MicroService as MS
from api.schemas.pydantic.LogsSchema import LogsSchema, LogsCreateSchema, LogsUpdateSchema


class LogsRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self, logs: LogsCreateSchema):
        verifs = self.verif_duplicate(logs)
        data = logs.dict()

        if len(verifs) == 0 :
            try:
                unique_id = {"unique_id":str(uuid.uuid1().hex)} # lie a l'adresse MAC du PC uuid4() n'est pas lié
                logs = data
                logs.update(unique_id)

                log = self.db.execute(insert(Logs), logs)
                stmt = select(Logs).where(Logs.unique_id == logs['unique_id'])
                log = self.db.scalars(stmt).one()
                self.db.commit()

            except Exception as e:
                raise HTTPException(status_code = 400, detail = {})

            return log
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})    

    def get(self, id: int, is_activated : bool = True):
        try:
            stmt = select(Logs).where(Logs.id == id, Logs.is_activated == is_activated)
            log = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})            

        status_code = add_log(MS.REFGEOGRAPHIQUE.value, "/", "GET", MS.USER.value, MS.PREVDATA.value, log, MS.STATUS.value)
            
        return log

    def get_id(self, id : int):
        try:
            log = self.db.get(Logs, id)
            if log ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return log

    def get_signature(self, signature: str, is_activated : bool = True):

        try:
            stmt = select(Logs).where(Logs.unique_id == signature, Logs.is_activated == is_activated)
            log = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return log

    def get_id_and_signature(self, id: int, signature: str, is_activated : bool = True):

        try:
            stmt = select(Logs).where(Logs.id == id, Logs.unique_id == signature, Logs.is_activated == is_activated)
            log = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return log


    def list(self, skip: int = 0, limit: int = 100):
        try:
            stmt = select(Logs).where(Logs.is_activated == True).offset(skip).limit(limit)
            logs = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return logs

    # microservice
    # endpoint
    # user_uid
    # user_email
    # verb
    # user
    # prev_data
    # data

    def update(self, log: LogsUpdateSchema):
        verif = self.verif_duplicate(log)
        data = log.dict()
        if len(verif) == 0 :
            logs = data
            try:
                stmt = (
                    update(Logs)
                    .where(Logs.id == logs['id'])
                    .values(infos = logs['infos'], updated_at = func.now())
                    # .values(microservice = logs['microservice'], endpoint = logs['endpoint'], user_uid = logs['user_uid'], user_email = logs['user_email'], 
                    # verb = logs['verb'], user = logs['user'], prev_data = logs['prev_data'], data = logs['data'], updated_at = func.now())
                )
                log = self.db.execute(stmt)
                log = self.get(logs['id'])
                self.db.commit()    
            except Exception as e:
                raise HTTPException(status_code=400, detail={})

            return log

        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})

    def delete(self, id : int, is_activated : bool = False):
        try:
            stmt = (
                update(Logs)
                .where(Logs.id == id)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(Logs)
            )
            log = self.db.execute(stmt)
            log = jsonable_encoder(log)
            log = self.db.get(Logs, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return log


    def delete_signature(self, id : int, signature : str, is_activated : bool = False):
        try:
            stmt = (
                update(Logs)
                .where(Logs.id == id, Logs.unique_id == signature)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(Logs)
            )
            log = self.db.execute(stmt)
            log = jsonable_encoder(log)
            # log = self.db.get(id)
            log = self.db.get(Logs, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return log

    def verif_duplicate(self, logs: LogsSchema):
        # id = logs.id if hasattr(logs, 'id') else 0
        # req ="Logs.id != " + str(id)
        # name = logs.infos['name'] if 'name' in logs.infos else ""

        # try:
        #     stmt = (
        #         select(Logs)
        #         .filter(Logs.infos['name'].as_string().ilike(name))
        #         .filter(eval(req))
        #     )
            
        #     log = self.db.scalars(stmt).all()

        # except Exception as e:
        #     raise HTTPException(status_code=400, detail={})

        # return log
        return []

    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, is_activated : bool = True):       
        try:
            stmt = (
                select(Logs)
                .where(Logs.is_activated == is_activated)
                # .filter(Logs.infos['code'].as_string().ilike(code) if code is not None else True)
                .filter(Logs.unique_id.like(signature) if signature is not None else True)
                .filter(Logs.id == id if id != 0 else True)
            )
            
            result = self.db.scalars(stmt).first()

            areas = result.areas

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg, "search" : {"id" : id, "code" : code,"signature" : signature}})

        return result



# import requests

# # r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
# # r = requests.get('http://127.0.0.1:8000/v1/regionaldelegation/', auth=('user', 'pass'))

# r = requests.post('http://127.0.0.1:8000/v1/regionaldelegation/', json = {"infos": {"name": "DR Taslim 1"}})

# print(r.status_code)
# print(r.headers['content-type'])
# print(r.encoding)
# # print(r.text)
# print(r.json())
