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
from api.models.RefCityLevelsModel import RefCityLevels
from api.schemas.pydantic.RefCityLevelsSchema import (RefCityLevelsSchema, RefCityLevelsCreateSchema, EXAMPLE, 
RefCityLevelsUpdateSchema, EXAMPLE1)

class RefCityLevelsRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self, ref_city_levels: RefCityLevelsCreateSchema):
        verif_city_levels = self.verif_duplicate(ref_city_levels)
        data = ref_city_levels.dict()

        if len(verif_city_levels) == 0 :
            try:
                unique_id = {"unique_id":str(uuid.uuid1().hex)} # lie a l'adresse MAC du PC uuid4() n'est pas lié
                ref_city_levels = data
                ref_city_levels.update(unique_id)
                # ref_city_levels['unique_id'] = unique_id

                ref_city_level = self.db.execute(insert(RefCityLevels), ref_city_levels)
                # ref_city_level = self.db.execute(insert(RefCityLevels), ref_city_levels.dict())
                stmt = select(RefCityLevels).where(RefCityLevels.unique_id == ref_city_levels['unique_id'])
                ref_city_level = self.db.scalars(stmt).one()
                self.db.commit()

            except Exception as e:
                raise HTTPException(status_code=400, detail={})

            return ref_city_level
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})

    def get(self, id: int, is_activated : bool = True):
        try:
            stmt = select(RefCityLevels).where(RefCityLevels.id == id, RefCityLevels.is_activated == is_activated)
            ref_city_level = self.db.scalars(stmt).one()
            # areas = ref_city_level.areas
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_city_level

    def get_id(self, id : int):
        try:
            ref_city_level = self.db.get(RefCityLevels, id)
            if ref_city_level ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_city_level

    def get_signature(self, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefCityLevels).where(RefCityLevels.unique_id == signature, RefCityLevels.is_activated == is_activated)
            ref_city_level = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_city_level

    def get_id_and_signature(self, id: int, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefCityLevels).where(RefCityLevels.id == id, RefCityLevels.unique_id == signature, RefCityLevels.is_activated == is_activated)
            ref_city_level = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_city_level

    def list(self, skip: int = 0, limit: int = 100):
        try:
            stmt = select(RefCityLevels).where(RefCityLevels.is_activated == True).offset(skip).limit(limit)
            ref_city_levels = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_city_levels

    def update(self, ref_city_levels: RefCityLevelsUpdateSchema):
        verif_city_levels = self.verif_duplicate(ref_city_levels)
        data = ref_city_levels.dict()
        if len(verif_city_levels) == 0 :
            city_levels = data
            try:
                stmt = (
                    update(RefCityLevels)
                    .where(RefCityLevels.id == city_levels['id'])
                    .values(name = city_levels['name'], infos = city_levels['infos'], updated_at = func.now())
                    # .returning(RefCityLevels)
                )
                ref_city_level = self.db.execute(stmt)
                ref_city_level = self.db.get(RefCityLevels, city_levels['id'])

                self.db.commit()
            except Exception as e:
                raise HTTPException(status_code = 400, detail = {})

            return ref_city_level
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})



    def delete(self, id : int, is_activated : bool = False):
        try:
            stmt = (
                update(RefCityLevels)
                .where(RefCityLevels.id == id)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefCityLevels)
            )
            ref_city_level = self.db.execute(stmt)
            # ref_city_level = jsonable_encoder(ref_city_level)
            ref_city_level = self.db.get(RefCityLevels, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_city_level


    def delete_signature(self, id : int, signature : str, is_activated : bool = False):
        try:
            stmt = (
                update(RefCityLevels)
                .where(RefCityLevels.id == id, RefCityLevels.unique_id == signature)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefCityLevels)
            )
            ref_city_level = self.db.execute(stmt)
            # ref_city_level = jsonable_encoder(ref_city_level)
            ref_city_level = self.db.get(RefCityLevels, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_city_level

    def verif_duplicate(self, city_levels: RefCityLevelsSchema):
        id = city_levels.id if hasattr(city_levels, 'id') else 0
        req ="RefCityLevels.id != " + str(id)

        name = city_levels.name if hasattr(city_levels, 'name') else ""        
        try:
            stmt = (
                select(RefCityLevels)
                .filter(RefCityLevels.name.ilike(name))
                .filter(eval(req))
            )
            
            city_levels = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return city_levels

    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, is_activated : bool = True):       
        try:
            stmt = (
                select(RefCityLevels)
                .where(RefCityLevels.is_activated == is_activated)
                # .filter(RefCityLevels.infos['code'].as_string().ilike(code) if code is not None else True)
                .filter(RefCityLevels.unique_id.like(signature) if signature is not None else True)
                .filter(RefCityLevels.id == id if id != 0 else True)
            )
            
            result = self.db.scalars(stmt).first()

            # areas = result.areas

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg, "search" : {"id" : id, "code" : code,"signature" : signature}})

        return result

