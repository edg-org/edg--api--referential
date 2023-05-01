from typing import List, Optional
import json
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, lazyload
from sqlalchemy import select, insert, update, delete, and_, or_
from fastapi.encoders import jsonable_encoder
import uuid
from sqlalchemy.sql import func
from api.configs.Database import (get_db_connection,)
from api.models.RefRegionalDelegationsModel import RefRegionalDelegations
from api.schemas.pydantic.RefRegionalDelegationsSchema import RefRegionalDelegationsSchema, RefRegionalDelegationsCreateSchema, RefRegionalDelegationsUpdateSchema

class RefRegionalDelegationsRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self, ref_regional_delegations: RefRegionalDelegationsCreateSchema):
        verif_regional_delegations = self.verif_duplicate(ref_regional_delegations)
        data = ref_regional_delegations.dict()
        if len(verif_regional_delegations) == 0 :
            try:
                code = self.code_generate()
                ref_regional_delegations = data
                ref_regional_delegations.update({"unique_id" : str(uuid.uuid1().hex)}) # lie a l'adresse MAC du PC uuid4() n'est pas lié
                ref_regional_delegations.update({"code" : int(code)})  
                ref_regional_delegations['infos'].update({"code": str(code)})

                ref_regional_delegation = self.db.execute(insert(RefRegionalDelegations), ref_regional_delegations)
                stmt = select(RefRegionalDelegations).where(RefRegionalDelegations.unique_id == ref_regional_delegations['unique_id'])
                ref_regional_delegation = self.db.scalars(stmt).one()
                self.db.commit()
            except Exception as e:
                raise HTTPException(status_code = 400, detail = {"msg" : "Recordmenet not performed", "data" : data})
            return ref_regional_delegation
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})

    
    def get(self, id: int, is_activated : bool = True):
        try:
            stmt = select(RefRegionalDelegations).where(RefRegionalDelegations.id == id, RefRegionalDelegations.is_activated == is_activated)
            ref_regional_delegation = self.db.scalars(stmt).one()
            # adm_regions = ref_regional_delegation.adm_regions # il faut tjr faire appel si on veut voir les elements enfants ou parent
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_regional_delegation

    def get_id(self, id : int):
        try:
            ref_regional_delegation = self.db.get(RefRegionalDelegations, id)
            if ref_regional_delegation ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_regional_delegation

    def get_signature(self, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefRegionalDelegations).where(RefRegionalDelegations.unique_id == signature, RefRegionalDelegations.is_activated == is_activated)
            ref_regional_delegation = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_regional_delegation

    def get_id_and_signature(self, id: int, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefRegionalDelegations).where(RefRegionalDelegations.id == id, RefRegionalDelegations.unique_id == signature, RefRegionalDelegations.is_activated == is_activated)
            ref_regional_delegation = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_regional_delegation

    def list(self, skip: int = 0, limit: int = 100):
        try:
            stmt = select(RefRegionalDelegations).where(RefRegionalDelegations.is_activated == True).offset(skip).limit(limit)
            ref_regional_delegations = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_regional_delegations

    def update(self, ref_regional_delegation: RefRegionalDelegationsUpdateSchema):
        verif_regional_delegation = self.verif_duplicate(ref_regional_delegation)
        data = ref_regional_delegation.dict()
        if len(verif_regional_delegation) == 0 :
            regional_delegation = data
            regional_delegation['infos'].update({"code": str(self.get_code_by_id(regional_delegation['id']))})
            try:
                stmt = (
                    update(RefRegionalDelegations)
                    .where(RefRegionalDelegations.id == regional_delegation['id'])
                    .values(infos = regional_delegation['infos'], updated_at = func.now())
                )
                ref_regional_delegation = self.db.execute(stmt)
                # ref_regional_delegation = jsonable_encoder(ref_regional_delegation)
                ref_regional_delegation = self.get(regional_delegation['id'])
                self.db.commit()    
                # ref_regional_delegations = self.db.execute(update(RefRegionalDelegations), [ref_regional_delegation.dict()])
            except Exception as e:
                raise HTTPException(status_code=400, detail={})

            return ref_regional_delegation

        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})

    def delete(self, id : int, is_activated : bool = False):
        try:
            stmt = (
                update(RefRegionalDelegations)
                .where(RefRegionalDelegations.id == id)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefRegionalDelegations)
            )
            ref_regional_delegation = self.db.execute(stmt)
            ref_regional_delegation = jsonable_encoder(ref_regional_delegation)
            ref_regional_delegation = self.db.get(RefRegionalDelegations, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_regional_delegation


    def delete_signature(self, id : int, signature : str, is_activated : bool = False):
        try:
            stmt = (
                update(RefRegionalDelegations)
                .where(RefRegionalDelegations.id == id, RefRegionalDelegations.unique_id == signature)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefRegionalDelegations)
            )
            ref_regional_delegation = self.db.execute(stmt)
            ref_regional_delegation = jsonable_encoder(ref_regional_delegation)
            # ref_regional_delegation = self.db.get(id)
            ref_regional_delegation = self.db.get(RefRegionalDelegations, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_regional_delegation

    def verif_duplicate(self, regional_delegation: RefRegionalDelegationsSchema):
        id = regional_delegation.id if hasattr(regional_delegation, 'id') else 0
        req ="RefRegionalDelegations.id != " + str(id)
        # name = regional_delegation.infos['name'] if 'name' in regional_delegation.infos else ""
        name = regional_delegation.infos.name if hasattr(regional_delegation.infos, 'name') else ""
        try:
            stmt = (
                select(RefRegionalDelegations)
                .filter(RefRegionalDelegations.infos['name'].as_string().ilike(name))
                .filter(eval(req))
            )
            
            ref_regional_delegation = self.db.scalars(stmt).all()

        except Exception as e:
            raise HTTPException(status_code = 400, detail = {})

        return ref_regional_delegation

    # def verif_duplicate(self, regional_delegation: RefRegionalDelegationsSchema):
    #     id = regional_delegation.id if hasattr(regional_delegation, 'id') else 0
    #     req ="RefRegionalDelegations.id != " + str(id)
    #     name = regional_delegation.infos.name if hasattr(regional_delegation.infos, 'name') else ""
    #     # name = regional_delegation.infos['name'] if 'name' in regional_delegation.infos else ""
    #     stmt = (
    #         select(RefRegionalDelegations)
    #         .filter(RefRegionalDelegations.infos['name'].as_string().ilike(name))
    #         .filter(eval(req))
    #     )
        
    #     ref_regional_delegation = self.db.scalars(stmt).all()
    #     return ref_regional_delegation





    def code_generate(self):
        count_query = select(func.count(RefRegionalDelegations.id))
        count_result = self.db.execute(count_query).scalar()
        count_result = count_result + 1
        # count_result = (count_result + 1) * 10
        if count_result < 10 : 
            count_result = "0" + str(count_result)
        return count_result

    def get_code_by_id(self, id : int):
        try:
            ref_regional_delegation = self.db.get(RefRegionalDelegations, id)
            if ref_regional_delegation ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_regional_delegation.infos['code']


    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, is_activated : bool = True):       
        try:
            stmt = (
                select(RefRegionalDelegations)
                .where(RefRegionalDelegations.is_activated == is_activated)
                .filter(RefRegionalDelegations.infos['code'].as_string().ilike(code) if code is not None else True)
                .filter(RefRegionalDelegations.unique_id.like(signature) if signature is not None else True)
                .filter(RefRegionalDelegations.id == id if id != 0 else True)
            )
            
            result = self.db.scalars(stmt).first()

            # adm_regions = result.adm_regions

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg, "search" : {"id" : id, "code" : code,"signature" : signature}})

        return result


