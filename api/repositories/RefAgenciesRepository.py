from typing import List, Optional
import json
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, lazyload
from sqlalchemy import select, insert, update, delete, and_
from fastapi.encoders import jsonable_encoder
import uuid
from sqlalchemy.sql import func

from api.configs.Database import (get_db_connection,)
from api.models.RefNaturalRegionsModel import RefNaturalRegions
from api.models.RefAgenciesModel import RefAgencies
from api.schemas.pydantic.RefAgenciesSchema import (RefAgenciesSchema, RefAgenciesCreateSchema, EXAMPLE, RefAgenciesUpdateSchema,
EXAMPLE1)


class RefAgenciesRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self, ref_agencies: RefAgenciesCreateSchema):
        verif_agencies = self.verif_duplicate(ref_agencies)
        data = ref_agencies.dict()
        if len(verif_agencies) == 0 :
            try:
                # ref_agencie = self.db.scalars(insert(RefAgencies).returning(RefAgencies), ref_agencies.dict()).first()            
                unique_id = {"unique_id": str(uuid.uuid1().hex)} # lie a l'adresse MAC du PC uuid4() n'est pas lié
                ref_agencies = data
                ref_agencies.update(unique_id)
                # ref_agencies['unique_id'] = unique_id

                ref_agencie = self.db.execute(insert(RefAgencies), ref_agencies)
                # ref_agencie = self.db.execute(insert(RefAgencies), ref_agencies.dict())
                stmt = select(RefAgencies).where(RefAgencies.unique_id == ref_agencies['unique_id'])
                ref_agencie = self.db.scalars(stmt).one()
                self.db.commit()

            except Exception as e:
                raise HTTPException(status_code=400, detail={})
                # self.db.rollback()

            return ref_agencie
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})
       

    def get(self, id: int, is_activated : bool = True):
        try:
            stmt = select(RefAgencies).where(RefAgencies.id == id, RefAgencies.is_activated == is_activated)
            ref_agencie = self.db.scalars(stmt).one()
            # areas = ref_agencie.areas
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_agencie


    def get_id(self, id : int):
        try:
            ref_agencie = self.db.get(RefAgencies, id)
            if ref_agencie ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_agencie

    def get_signature(self, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefAgencies).where(RefAgencies.unique_id == signature, RefAgencies.is_activated == is_activated)
            ref_agencie = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_agencie

    def get_id_and_signature(self, id: int, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefAgencies).where(RefAgencies.id == id, RefAgencies.unique_id == signature, RefAgencies.is_activated == is_activated)
            ref_agencie = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_agencie

    def list(self, skip: int = 0, limit: int = 100):
        try:
            stmt = select(RefAgencies).where(RefAgencies.is_activated == True).offset(skip).limit(limit)
            ref_agencies = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_agencies

    def update(self, ref_agencies: RefAgenciesUpdateSchema):
        verif_agencies = self.verif_duplicate(ref_agencies)
        data = ref_agencies.dict()
        if len(verif_agencies) == 0 :
            agencies = data
            try:
                stmt = (
                    update(RefAgencies)
                    .where(RefAgencies.id == agencies['id'])
                    .values(areas_id = agencies['areas_id'], infos = agencies['infos'], updated_at = func.now())
                    # .returning(RefAgencies)
                )
                ref_agencie = self.db.execute(stmt)
                # ref_agencie = self.db.scalars(stmt)
                # ref_agencie = jsonable_encoder(ref_agencie)
                ref_agencie = self.get(agencies['id'])
                self.db.commit()
            except Exception as e:
                raise HTTPException(status_code=400, detail={})

            return ref_agencie
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})

    def delete(self, id : int, is_activated : bool = False):
        try:
            stmt = (
                update(RefAgencies)
                .where(RefAgencies.id == id)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefAgencies)
            )
            ref_agencie = self.db.execute(stmt)
            # ref_agencie = jsonable_encoder(ref_agencie)
            ref_agencie = self.db.get(RefAgencies, id)

            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_agencie


    def delete_signature(self, id : int, signature : str, is_activated : bool = False):
        try:
            stmt = (
                update(RefAgencies)
                .where(RefAgencies.id == id, RefAgencies.unique_id == signature)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefAgencies)
            )
            ref_agencie = self.db.execute(stmt)
            # ref_agencie = jsonable_encoder(ref_agencie)
            ref_agencie = self.db.get(RefAgencies, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_agencie


    def verif_duplicate(self, agencies: RefAgenciesSchema):
        id = agencies.id if hasattr(agencies, 'id') else 0
        areas_id = agencies.areas_id if hasattr(agencies, 'areas_id') else 0        
        req ="RefAgencies.id != " + str(id)
        name = agencies.infos.name if hasattr(agencies.infos, 'name') else ""
        # name = agencies.infos['name'] if 'name' in agencies.infos else ""
        try:
            stmt = (
                select(RefAgencies)
                .filter(RefAgencies.infos['name'].as_string().ilike(name), RefAgencies.areas_id == areas_id)
                .filter(eval(req))
            )
            
            agencies = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code = 400, detail={})

        return agencies


    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, is_activated : bool = True):       
        try:
            stmt = (
                select(RefAgencies)
                .where(RefAgencies.is_activated == is_activated)
                .filter(RefAgencies.infos['code'].as_string().ilike(code) if code is not None else True)
                .filter(RefAgencies.unique_id.like(signature) if signature is not None else True)
                .filter(RefAgencies.id == id if id != 0 else True)
            )
            
            result = self.db.scalars(stmt).first()

            areas = result.areas

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg, "search" : {"id" : id, "code" : code,"signature" : signature}})

        return result


