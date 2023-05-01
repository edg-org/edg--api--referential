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
from api.models.RefPrefecturesModel import RefPrefectures
from api.schemas.pydantic.RefNaturalRegionsSchema import RefNaturalRegionsSchema, RefNaturalRegionsCreateSchema
from api.schemas.pydantic.RefPrefecturesSchema import (RefPrefecturesSchema, RefPrefecturesCreateSchema, EXAMPLE,
RefPrefecturesUpdateSchema, EXAMPLE1)
from api.repositories.RefAdmRegionsRepository import RefAdmRegionsRepository

class RefPrefecturesRepository:
    db: Session
    region_repository : RefAdmRegionsRepository

    def __init__(self, region_repository: RefAdmRegionsRepository = Depends(), db: Session = Depends(get_db_connection)) -> None:
        self.db = db
        self.region_repository = region_repository

    def create(self, ref_prefectures: RefPrefecturesCreateSchema):
        verif_prefectures = self.verif_duplicate(ref_prefectures)
        data = ref_prefectures.dict()
        if len(verif_prefectures) == 0 :

            try:
                ref_prefectures = data
                code = self.code_generate(ref_prefectures['region_id'])
                ref_prefectures.update({"unique_id" : str(uuid.uuid1().hex)}) # lie a l'adresse MAC du PC uuid4() n'est pas lié 
                ref_prefectures.update({"code" : int(code)})  
                ref_prefectures['infos'].update({"code": str(code)})

                ref_prefecture = self.db.execute(insert(RefPrefectures), ref_prefectures)
               
                stmt = select(RefPrefectures).where(RefPrefectures.unique_id == ref_prefectures['unique_id'])
                ref_prefecture = self.db.scalars(stmt).one()
                self.db.commit()

            except Exception as e:
                raise HTTPException(status_code=400, detail={})

            return ref_prefecture
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})


    def get(self, id: int, is_activated : bool = True):
        try:
            stmt = select(RefPrefectures).where(RefPrefectures.id == id, RefPrefectures.is_activated == is_activated)
            ref_prefecture = self.db.scalars(stmt).one()
            # adm_region = ref_prefecture.adm_region
            # prefectures = ref_prefecture.prefectures
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_prefecture


    def get_id(self, id : int):
        try:
            ref_prefecture = self.db.get(RefPrefectures, id)
            if ref_prefecture ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_prefecture

    def get_signature(self, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefPrefectures).where(RefPrefectures.unique_id == signature, RefPrefectures.is_activated == is_activated)
            ref_prefecture = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_prefecture

    def get_id_and_signature(self, id: int, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefPrefectures).where(RefPrefectures.id == id, RefPrefectures.unique_id == signature, RefPrefectures.is_activated == is_activated)
            ref_prefecture = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_prefecture

    def list(self, skip: int = 0, limit: int = 100):
        try:
            stmt = select(RefPrefectures).where(RefPrefectures.is_activated == True).offset(skip).limit(limit)
            ref_prefectures = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_prefectures

    def update(self, ref_prefectures: RefPrefecturesUpdateSchema):
        verif_prefectures = self.verif_duplicate(ref_prefectures)
        data = ref_prefectures.dict()
        if len(verif_prefectures) == 0 :
            prefectures = data
            prefectures['infos'].update({"code": str(self.get_code_by_id(prefectures['id']))})
            try:
                stmt = (
                    update(RefPrefectures)
                    .where(RefPrefectures.id == prefectures['id'])
                    .values(region_id = prefectures['region_id'], infos = prefectures['infos'], updated_at = func.now())
                    # .returning(RefPrefectures)
                )
                ref_prefecture = self.db.execute(stmt)
                # ref_prefecture = self.db.scalars(stmt)
                # ref_prefecture = jsonable_encoder(ref_prefecture)
                ref_prefecture = self.get(prefectures['id'])
                self.db.commit()
            except Exception as e:
                raise HTTPException(status_code=400, detail={})

            return ref_prefecture
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})



    def delete(self, id : int, is_activated : bool = False):
        try:
            stmt = (
                update(RefPrefectures)
                .where(RefPrefectures.id == id)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefPrefectures)
            )
            ref_prefecture = self.db.execute(stmt)
            # ref_prefecture = jsonable_encoder(ref_prefecture)
            ref_prefecture = self.db.get(RefPrefectures, id)

            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_prefecture


    def delete_signature(self, id : int, signature : str, is_activated : bool = False):
        try:
            stmt = (
                update(RefPrefectures)
                .where(RefPrefectures.id == id, RefPrefectures.unique_id == signature)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefPrefectures)
            )
            ref_prefecture = self.db.execute(stmt)
            # ref_prefecture = jsonable_encoder(ref_prefecture)
            ref_prefecture = self.db.get(RefPrefectures, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_prefecture

    def verif_duplicate(self, prefectures: RefPrefecturesSchema):
        id = prefectures.id if hasattr(prefectures, 'id') else 0
        region_id = prefectures.region_id if hasattr(prefectures, 'region_id') else 0        
        req ="RefPrefectures.id != " + str(id)
        # name = prefectures.infos['name'] if 'name' in prefectures.infos else ""
        name = prefectures.infos.name if hasattr(prefectures.infos, 'name') else ""
        try:
            stmt = (
                select(RefPrefectures)
                .filter(RefPrefectures.infos['name'].as_string().ilike(name), RefPrefectures.region_id == region_id)
                .filter(eval(req))
            )
            
            prefectures = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return prefectures

    def get_code_by_id(self, id : int):
        try:
            ref_prefecture = self.db.get(RefPrefectures, id)
            if ref_prefecture ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_prefecture.infos['code']

    def code_generate(self, region_id : int):
        region_code = self.region_repository.get_code_by_id(region_id)

        count_query = select(func.count(RefPrefectures.id)).where(RefPrefectures.region_id == region_id)
        count_result = self.db.execute(count_query).scalar()
        count_result = (int(region_code) * 100) + (count_result + 1)
        return count_result


    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, is_activated : bool = True):       
        try:
            stmt = (
                select(RefPrefectures)
                .where(RefPrefectures.is_activated == is_activated)
                .filter(RefPrefectures.infos['code'].as_string().ilike(code) if code is not None else True)
                .filter(RefPrefectures.unique_id.like(signature) if signature is not None else True)
                .filter(RefPrefectures.id == id if id != 0 else True)
            )
            
            result = self.db.scalars(stmt).first()
            adm_region = result.adm_region
            cities = result.cities

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg, "search" : {"id" : id, "code" : code,"signature" : signature}})

        return result


