from typing import List, Optional
import json
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, lazyload
from sqlalchemy import select, insert, update, delete, and_, or_
from fastapi.encoders import jsonable_encoder
import uuid
from sqlalchemy.sql import func
from api.configs.Database import (get_db_connection,)
from api.models.RefMicroServicesModel import RefMicroServices
from api.schemas.pydantic.RefMicroServicesSchema import RefMicroServicesSchema, RefMicroServicesCreateSchema, RefMicroServicesUpdateSchema

class RefMicroServicesRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self, ref_micro_services: RefMicroServicesCreateSchema):
        verif_micro_services = self.verif_duplicate(ref_micro_services)
        data = ref_micro_services.dict()
        if len(verif_micro_services) == 0 :
            try:
                ref_micro_services = data
                ref_micro_services.update({"unique_id":str(uuid.uuid1().hex)}) # lie a l'adresse MAC du PC uuid4() n'est pas lié
                ref_micro_services['infos'].update({"code": str(self.code_generate())})

                ref_micro_service = self.db.execute(insert(RefMicroServices), ref_micro_services)
                stmt = select(RefMicroServices).where(RefMicroServices.unique_id == ref_micro_services['unique_id'])
                ref_micro_service = self.db.scalars(stmt).one()
                self.db.commit()
            except Exception as e:
                raise HTTPException(status_code = 400, detail = {"msg" : "Recordmenet not performed", "data" : data})
            return ref_micro_service
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})
    
    def get(self, id: int, is_activated : bool = True):
        try:
            stmt = select(RefMicroServices).where(RefMicroServices.id == id, RefMicroServices.is_activated == is_activated)
            ref_micro_service = self.db.scalars(stmt).one()
            # adm_regions = ref_micro_service.adm_regions # il faut tjr faire appel si on veut voir les elements enfants ou parent
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_micro_service

    def get_id(self, id : int):
        try:
            ref_micro_service = self.db.get(RefMicroServices, id)
            if ref_micro_service ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_micro_service

    def get_signature(self, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefMicroServices).where(RefMicroServices.unique_id == signature, RefMicroServices.is_activated == is_activated)
            ref_micro_service = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_micro_service

    def get_id_and_signature(self, id: int, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefMicroServices).where(RefMicroServices.id == id, RefMicroServices.unique_id == signature, RefMicroServices.is_activated == is_activated)
            ref_micro_service = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_micro_service

    def list(self, skip: int = 0, limit: int = 100):
        try:
            stmt = select(RefMicroServices).where(RefMicroServices.is_activated == True).offset(skip).limit(limit)
            ref_micro_services = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_micro_services

    def update(self, ref_micro_service: RefMicroServicesUpdateSchema):
        verif_micro_service = self.verif_duplicate(ref_micro_service)
        data = ref_micro_service.dict()
        if len(verif_micro_service) == 0 :
            micro_service = data
            micro_service['infos'].update({"code": str(self.get_code_by_id(micro_service['id']))})
            try:
                stmt = (
                    update(RefMicroServices)
                    .where(RefMicroServices.id == micro_service['id'])
                    .values(infos = micro_service['infos'], updated_at = func.now())
                )
                ref_micro_service = self.db.execute(stmt)
                # ref_micro_service = jsonable_encoder(ref_micro_service)
                ref_micro_service = self.get(micro_service['id'])
                self.db.commit()    
                # ref_micro_services = self.db.execute(update(RefMicroServices), [ref_micro_service.dict()])
            except Exception as e:
                raise HTTPException(status_code=400, detail={})

            return ref_micro_service

        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})

    def delete(self, id : int, is_activated : bool = False):
        try:
            stmt = (
                update(RefMicroServices)
                .where(RefMicroServices.id == id)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefMicroServices)
            )
            ref_micro_service = self.db.execute(stmt)
            ref_micro_service = jsonable_encoder(ref_micro_service)
            ref_micro_service = self.db.get(RefMicroServices, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_micro_service


    def delete_signature(self, id : int, signature : str, is_activated : bool = False):
        try:
            stmt = (
                update(RefMicroServices)
                .where(RefMicroServices.id == id, RefMicroServices.unique_id == signature)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefMicroServices)
            )
            ref_micro_service = self.db.execute(stmt)
            ref_micro_service = jsonable_encoder(ref_micro_service)
            # ref_micro_service = self.db.get(id)
            ref_micro_service = self.db.get(RefMicroServices, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_micro_service

    def verif_duplicate(self, micro_service: RefMicroServicesSchema):
        id = micro_service.id if hasattr(micro_service, 'id') else 0
        req ="RefMicroServices.id != " + str(id)
        # name = micro_service.infos['name'] if 'name' in micro_service.infos else ""
        name = micro_service.infos.name if hasattr(micro_service.infos, 'name') else ""
        try:
            stmt = (
                select(RefMicroServices)
                .filter(RefMicroServices.infos['name'].as_string().ilike(name))
                .filter(eval(req))
            )
            
            ref_micro_service = self.db.scalars(stmt).all()

        except Exception as e:
            raise HTTPException(status_code = 400, detail={})

        return ref_micro_service

    def code_generate(self):
        count_query = select(func.count(RefMicroServices.id))
        count_result = self.db.execute(count_query).scalar()
        count_result = count_result + 1
        # count_result = (count_result + 1) * 10
        if count_result < 10 : 
            count_result = "0" + str(count_result)
        return count_result

    def get_code_by_id(self, id : int):
        try:
            ref_micro_service = self.db.get(RefMicroServices, id)
            if ref_micro_service ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_micro_service.infos['code']


    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, is_activated : bool = True):       
        try:
            stmt = (
                select(RefMicroServices)
                .where(RefMicroServices.is_activated == is_activated)
                .filter(RefMicroServices.infos['code'].as_string().ilike(code) if code is not None else True)
                .filter(RefMicroServices.unique_id.like(signature) if signature is not None else True)
                .filter(RefMicroServices.id == id if id != 0 else True)
            )
            
            result = self.db.scalars(stmt).first()

            # adm_regions = result.adm_regions

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg, "search" : {"id" : id, "code" : code,"signature" : signature}})

        return result


