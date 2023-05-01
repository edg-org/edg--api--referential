from typing import List, Optional
import json
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, lazyload
from sqlalchemy import select, insert, update, delete, and_, or_
from fastapi.encoders import jsonable_encoder
import uuid
from sqlalchemy.sql import func
from api.configs.Database import (get_db_connection,)
from api.models.RefNaturalRegionsModel import RefNaturalRegions
from api.models.RefAdmRegionsModel import RefAdmRegions
from api.schemas.pydantic.RefNaturalRegionsSchema import RefNaturalRegionsSchema, RefNaturalRegionsCreateSchema
from api.schemas.pydantic.RefAdmRegionsSchema import (RefAdmRegionsSchema, RefAdmRegionsCreateSchema, EXAMPLE,
RefAdmRegionsUpdateSchema, EXAMPLE1, RefAdmRegionsSearchSchema)
from api.repositories.RefNaturalRegionsRepository import RefNaturalRegionsRepository

class RefAdmRegionsRepository:
    db: Session
    natural_region_repository : RefNaturalRegionsRepository

    def __init__(self, natural_region_repository: RefNaturalRegionsRepository = Depends(), db: Session = Depends(get_db_connection)) -> None:
        self.db = db
        self.natural_region_repository = natural_region_repository

    def create(self, ref_adm_regions: RefAdmRegionsCreateSchema):
        verif_adm_regions = self.verif_duplicate(ref_adm_regions)
        data = ref_adm_regions.dict()

        if len(verif_adm_regions) == 0 :
            try:
                ref_adm_regions = data
                code = self.code_generate(ref_adm_regions['natural_region_id'])
                ref_adm_regions.update({"unique_id" : str(uuid.uuid1().hex)}) # lie a l'adresse MAC du PC uuid4() n'est pas lié
                ref_adm_regions.update({"code" : int(code)})  
                ref_adm_regions['infos'].update({"code": str(code)})

                ref_adm_region = self.db.execute(insert(RefAdmRegions), ref_adm_regions)
                # ref_adm_region = self.db.execute(insert(RefAdmRegions), ref_adm_regions.dict())
                stmt = select(RefAdmRegions).where(RefAdmRegions.unique_id == ref_adm_regions['unique_id'])
                ref_adm_region = self.db.scalars(stmt).one()
                self.db.commit()

            except Exception as e:
                raise HTTPException(status_code=400, detail={})

            return ref_adm_region
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})

    def get(self, id: int, is_activated : bool = True):
        try:
            stmt = select(RefAdmRegions).where(RefAdmRegions.id == id, RefAdmRegions.is_activated == is_activated)
            ref_adm_region = self.db.scalars(stmt).one()
            # natural_region = ref_adm_region.natural_region
            # prefectures = ref_adm_region.prefectures
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_adm_region

    def get_id(self, id : int):
        try:
            ref_adm_region = self.db.get(RefAdmRegions, id)
            if ref_adm_region ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_adm_region

    def get_signature(self, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefAdmRegions).where(RefAdmRegions.unique_id == signature, RefAdmRegions.is_activated == is_activated)
            ref_adm_region = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_adm_region

    def get_id_and_signature(self, id: int, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefAdmRegions).where(RefAdmRegions.id == id, RefAdmRegions.unique_id == signature, RefAdmRegions.is_activated == is_activated)
            ref_adm_region = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_adm_region



    def list(self, skip: int = 0, limit: int = 100):
        try:
            stmt = select(RefAdmRegions).where(RefAdmRegions.is_activated == True).offset(skip).limit(limit)
            ref_adm_regions = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_adm_regions

    def update(self, ref_adm_regions: RefAdmRegionsUpdateSchema):
        verif_adm_regions = self.verif_duplicate(ref_adm_regions)
        data = ref_adm_regions.dict()

        if len(verif_adm_regions) == 0 :
            adm_regions = data
            adm_regions['infos'].update({"code": str(self.get_code_by_id(adm_regions['id']))})
            try:
                stmt = (
                    update(RefAdmRegions)
                    .where(RefAdmRegions.id == adm_regions['id'])
                    .values(natural_region_id = adm_regions['natural_region_id'], infos = adm_regions['infos'], updated_at = func.now())
                    # .returning(RefAdmRegions)
                )
                ref_adm_region = self.db.execute(stmt)
                # ref_adm_region = jsonable_encoder(ref_adm_region)
                ref_adm_region = self.get(adm_regions['id'])

                self.db.commit()

            except Exception as e:
                raise HTTPException(status_code=400, detail={})

            return ref_adm_region

        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})


    def delete(self, id : int, is_activated : bool = False):
        try:
            stmt = (
                update(RefAdmRegions)
                .where(RefAdmRegions.id == id)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefAdmRegions)
            )
            ref_adm_region = self.db.execute(stmt)
            # ref_adm_region = jsonable_encoder(ref_adm_region)
            ref_adm_region = self.db.get(RefAdmRegions, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_adm_region


    def delete_signature(self, id : int, signature : str, is_activated : bool = False):
        try:
            stmt = (
                update(RefAdmRegions)
                .where(RefAdmRegions.id == id, RefAdmRegions.unique_id == signature)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefAdmRegions)
            )
            ref_adm_region = self.db.execute(stmt)
            # ref_adm_region = jsonable_encoder(ref_adm_region)
            ref_adm_region = self.db.get(RefAdmRegions, id)

            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_adm_region

    def verif_duplicate(self, adm_regions : RefAdmRegionsSchema, update_status = 0):
        id = adm_regions.id if hasattr(adm_regions, 'id') else 0
        natural_region_id = adm_regions.natural_region_id if hasattr(adm_regions, 'natural_region_id') else 0        
        # natural_region_id = adm_regions.natural_region_id if adm_regions.natural_region_id else 0
        # name = adm_regions.infos['name'] if 'name' in adm_regions.infos else ""
        name = adm_regions.infos.name if hasattr(adm_regions.infos, 'name') else ""        
        req ="RefAdmRegions.id != " + str(id)

        try:
            stmt = (
                select(RefAdmRegions)
                .filter(RefAdmRegions.infos['name'].as_string().ilike(name), RefAdmRegions.natural_region_id == natural_region_id)
                .filter(eval(req))
            )
            
            adm_regions = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code = 400, detail = {})

        return adm_regions

    def get_code_by_id(self, id : int):
        try:
            ref_adm_region = self.db.get(RefAdmRegions, id)
            if ref_adm_region ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_adm_region.infos['code']

    def code_generate(self, natural_region_id : int):
        natural_region_code = self.natural_region_repository.get_code_by_id(natural_region_id)

        count_query = select(func.count(RefAdmRegions.id)).where(RefAdmRegions.natural_region_id == natural_region_id)
        count_result = self.db.execute(count_query).scalar()
        count_result = (int(natural_region_code) * 10) + (count_result + 1)
        return count_result

    # def get_items(self, item : RefAdmRegionsSearchSchema, is_activated : bool = True):       
    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, is_activated : bool = True):       
        try:
            stmt = (
                select(RefAdmRegions)
                .where(RefAdmRegions.is_activated == is_activated)
                .filter(RefAdmRegions.infos['code'].as_string().ilike(code) if code is not None else True)
                .filter(RefAdmRegions.unique_id.like(signature) if signature is not None else True)
                .filter(RefAdmRegions.id == id if id != 0 else True)
                # .filter(RefAdmRegions.id == id if id is not None else True)
            )
            
            result = self.db.scalars(stmt).first()

            natural_region = result.natural_region
            prefectures = result.prefectures

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg, "search" : {"id" : id, "code" : code,"signature" : signature}})

        return result

