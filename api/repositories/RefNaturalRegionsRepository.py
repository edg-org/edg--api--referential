from typing import List, Optional
import json
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, lazyload
from sqlalchemy import select, insert, update, delete, and_, or_
from fastapi.encoders import jsonable_encoder
import uuid
from api.internal.Admin import add_log, MicroService as MS
from sqlalchemy.sql import func
from api.configs.Database import (get_db_connection,)
from api.models.RefNaturalRegionsModel import RefNaturalRegions
from api.schemas.pydantic.RefNaturalRegionsSchema import RefNaturalRegionsSchema, RefNaturalRegionsCreateSchema, RefNaturalRegionsUpdateSchema

class RefNaturalRegionsRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self, ref_natural_regions: RefNaturalRegionsCreateSchema):
        verif_natural_regions = self.verif_duplicate(ref_natural_regions)
        data = ref_natural_regions.dict()
        if len(verif_natural_regions) == 0 :
            try:
                code = self.code_generate()
                ref_natural_regions = data
                ref_natural_regions.update({"unique_id" : str(uuid.uuid1().hex)}) # lie a l'adresse MAC du PC uuid4() n'est pas lié
                ref_natural_regions.update({"code" : int(code)})  
                ref_natural_regions['infos'].update({"code": str(code)})

                ref_natural_region = self.db.execute(insert(RefNaturalRegions), ref_natural_regions)
                stmt = select(RefNaturalRegions).where(RefNaturalRegions.unique_id == ref_natural_regions['unique_id'])
                ref_natural_region = self.db.scalars(stmt).one()
                status_code = add_log(MS.REFGEOGRAPHIQUE.value, "/", "POST", MS.USER.value, MS.PREVDATA.value, ref_natural_region, MS.STATUS.value)
                self.db.commit()
            except Exception as e:
                raise HTTPException(status_code = 400, detail = {"msg" : "Recordmenet not performed", "data" : data})

            return ref_natural_region
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})
    
    def get(self, id: int, is_activated : bool = True, is_log = False):
        try:
            stmt = select(RefNaturalRegions).where(RefNaturalRegions.id == id, RefNaturalRegions.is_activated == is_activated)
            ref_natural_region = self.db.scalars(stmt).one()
            # adm_regions = ref_natural_region.adm_regions # il faut tjr faire appel si on veut voir les elements enfants ou parent
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        if is_log == True: 
            status_code = add_log(MS.REFGEOGRAPHIQUE.value, "/", "GET", MS.USER.value, MS.PREVDATA.value, ref_natural_region, MS.STATUS.value)

        return ref_natural_region

    def get_id(self, id : int):
        try:
            ref_natural_region = self.db.get(RefNaturalRegions, id)
            if ref_natural_region ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_natural_region

    def get_signature(self, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefNaturalRegions).where(RefNaturalRegions.unique_id == signature, RefNaturalRegions.is_activated == is_activated)
            ref_natural_region = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_natural_region

    def get_id_and_signature(self, id: int, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefNaturalRegions).where(RefNaturalRegions.id == id, RefNaturalRegions.unique_id == signature, RefNaturalRegions.is_activated == is_activated)
            ref_natural_region = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_natural_region

    def list(self, skip: int = 0, limit: int = 100):
        try:
            stmt = select(RefNaturalRegions).where(RefNaturalRegions.is_activated == True).offset(skip).limit(limit)
            ref_natural_regions = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_natural_regions

    def update(self, ref_natural_region: RefNaturalRegionsUpdateSchema):
        verif_natural_region = self.verif_duplicate(ref_natural_region)
        data = ref_natural_region.dict()
        if len(verif_natural_region) == 0 :
            natural_region = data
            prev_natural_region = jsonable_encoder(self.get_id(natural_region['id']))
            natural_region['infos'].update({"code": str(self.get_code_by_id(natural_region['id']))})
            try:
                stmt = (
                    update(RefNaturalRegions)
                    .where(RefNaturalRegions.id == natural_region['id'])
                    .values(infos = natural_region['infos'], updated_at = func.now())
                )
                ref_natural_region = self.db.execute(stmt)
                ref_natural_region = self.get_id(natural_region['id'])
                # ref_natural_regions = self.db.execute(update(RefNaturalRegions), [ref_natural_region.dict()])

                status_code = add_log(MS.REFGEOGRAPHIQUE.value, "/", "PUT", MS.USER.value, prev_natural_region, ref_natural_region, MS.STATUS.value)
                self.db.commit()  
            except Exception as e:
                raise HTTPException(status_code=400, detail = {})

            return ref_natural_region

        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})

    def delete(self, id : int, is_activated : bool = False):
        try:
            prev_natural_region = jsonable_encoder(self.get_id(id))
            stmt = (
                update(RefNaturalRegions)
                .where(RefNaturalRegions.id == id)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefNaturalRegions)
            )
            ref_natural_region = self.db.execute(stmt)
            ref_natural_region = jsonable_encoder(ref_natural_region)
            ref_natural_region = self.db.get(RefNaturalRegions, id)
            status_code = add_log(MS.REFGEOGRAPHIQUE.value, "/", "DELETE", MS.USER.value, prev_natural_region, ref_natural_region, MS.STATUS.value)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_natural_region

    def delete_signature(self, id : int, signature : str, is_activated : bool = False):
        try:
            prev_natural_region = jsonable_encoder(self.get_id(id))
            stmt = (
                update(RefNaturalRegions)
                .where(RefNaturalRegions.id == id, RefNaturalRegions.unique_id == signature)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefNaturalRegions)
            )
            ref_natural_region = self.db.execute(stmt)
            ref_natural_region = jsonable_encoder(ref_natural_region)
            # ref_natural_region = self.db.get(id)
            ref_natural_region = self.db.get(RefNaturalRegions, id)
            status_code = add_log(MS.REFGEOGRAPHIQUE.value, "/", "DELETE", MS.USER.value, prev_natural_region, ref_natural_region, MS.STATUS.value)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_natural_region

    def verif_duplicate(self, natural_region: RefNaturalRegionsSchema):
        id = natural_region.id if hasattr(natural_region, 'id') else 0
        req ="RefNaturalRegions.id != " + str(id)
        name = natural_region.infos.name if hasattr(natural_region.infos, 'name') else ""
        # name = natural_region.infos['name'] if 'name' in natural_region.infos else ""

        try:
            stmt = (
                select(RefNaturalRegions)
                .filter(RefNaturalRegions.infos['name'].as_string().ilike(name))
                .filter(eval(req))
            )
            
            ref_natural_region = self.db.scalars(stmt).all()

        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_natural_region


    def code_generate(self):
        count_query = select(func.count(RefNaturalRegions.id))
        count_result = self.db.execute(count_query).scalar()
        count_result = (count_result + 1) * 10
        return count_result

    def get_code_by_id(self, id : int):
        try:
            ref_natural_region = self.db.get(RefNaturalRegions, id)
            if ref_natural_region ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_natural_region.infos['code']

    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, is_activated : bool = True):       
        try:
            stmt = (
                select(RefNaturalRegions)
                .where(RefNaturalRegions.is_activated == is_activated)
                .filter(RefNaturalRegions.infos['code'].as_string().ilike(code) if code is not None else True)
                .filter(RefNaturalRegions.unique_id.like(signature) if signature is not None else True)
                .filter(RefNaturalRegions.id == id if id != 0 else True)
            )
            
            result = self.db.scalars(stmt).first()

            adm_regions = result.adm_regions

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg, "search" : {"id" : id, "code" : code,"signature" : signature}})

        return result


