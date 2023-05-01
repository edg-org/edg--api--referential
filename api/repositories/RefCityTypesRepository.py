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
from api.models.RefCityTypesModel import RefCityTypes
from api.schemas.pydantic.RefCityTypesSchema import (RefCityTypesSchema, RefCityTypesCreateSchema, EXAMPLE, RefCityTypesUpdateSchema, EXAMPLE1)

class RefCityTypesRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self, ref_city_types: RefCityTypesCreateSchema):
        verif_city_types = self.verif_duplicate(ref_city_types)
        data = ref_city_types.dict()

        if len(verif_city_types) == 0 :
            try:
                unique_id = {"unique_id":str(uuid.uuid1().hex)} # lie a l'adresse MAC du PC uuid4() n'est pas lié
                ref_city_types = data
                ref_city_types.update(unique_id)
                # ref_city_types['unique_id'] = unique_id

                ref_city_type = self.db.execute(insert(RefCityTypes), ref_city_types)
                # ref_city_type = self.db.execute(insert(RefCityTypes), ref_city_types.dict())
                stmt = select(RefCityTypes).where(RefCityTypes.unique_id == ref_city_types['unique_id'])
                ref_city_type = self.db.scalars(stmt).one()
                self.db.commit()

            except Exception as e:
                raise HTTPException(status_code=400, detail={})

            return ref_city_type
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})

    def get(self, id: int, is_activated : bool = True):
        try:
            stmt = select(RefCityTypes).where(RefCityTypes.id == id, RefCityTypes.is_activated == is_activated)
            ref_city_type = self.db.scalars(stmt).one()
            # areas = ref_city_type.areas
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_city_type

    def get_id(self, id : int):
        try:
            ref_city_type = self.db.get(RefCityTypes, id)
            if ref_city_type ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_city_type

    def get_signature(self, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefCityTypes).where(RefCityTypes.unique_id == signature, RefCityTypes.is_activated == is_activated)
            ref_city_type = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_city_type

    def get_id_and_signature(self, id: int, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefCityTypes).where(RefCityTypes.id == id, RefCityTypes.unique_id == signature, RefCityTypes.is_activated == is_activated)
            ref_city_type = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_city_type

    def list(self, skip: int = 0, limit: int = 100):
        try:
            stmt = select(RefCityTypes).where(RefCityTypes.is_activated == True).offset(skip).limit(limit)
            ref_city_types = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_city_types

    def update(self, ref_city_types: RefCityTypesUpdateSchema):
        verif_city_types = self.verif_duplicate(ref_city_types)
        data = ref_city_types.dict()
        if len(verif_city_types) == 0 :
            city_types = data
            try:
                stmt = (
                    update(RefCityTypes)
                    .where(RefCityTypes.id == city_types['id'])
                    .values(name = city_types['name'], infos = city_types['infos'], updated_at = func.now())
                    # .returning(RefCityTypes)
                )
                ref_city_type = self.db.execute(stmt)
                ref_city_type = self.db.get(RefCityTypes, city_types['id'])

                self.db.commit()
            except Exception as e:
                raise HTTPException(status_code = 400, detail = {})

            return ref_city_type
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})

    def delete(self, id : int, is_activated : bool = False):
        try:
            stmt = (
                update(RefCityTypes)
                .where(RefCityTypes.id == id)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefCityTypes)
            )
            ref_city_type = self.db.execute(stmt)
            # ref_city_type = jsonable_encoder(ref_city_type)
            ref_city_type = self.db.get(RefCityTypes, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_city_type

    def delete_signature(self, id : int, signature : str, is_activated : bool = False):
        try:
            stmt = (
                update(RefCityTypes)
                .where(RefCityTypes.id == id, RefCityTypes.unique_id == signature)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefCityTypes)
            )
            ref_city_type = self.db.execute(stmt)
            # ref_city_type = jsonable_encoder(ref_city_type)
            ref_city_type = self.db.get(RefCityTypes, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_city_type

    def verif_duplicate(self, city_types: RefCityTypesSchema):
        id = city_types.id if hasattr(city_types, 'id') else 0
        req ="RefCityTypes.id != " + str(id)

        name = city_types.name if hasattr(city_types, 'name') else ""        
        try:
            stmt = (
                select(RefCityTypes)
                .filter(RefCityTypes.name.ilike(name))
                .filter(eval(req))
            )
            
            city_types = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return city_types

    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, is_activated : bool = True):       
        try:
            stmt = (
                select(RefCityTypes)
                .where(RefCityTypes.is_activated == is_activated)
                # .filter(RefCityTypes.infos['code'].as_string().ilike(code) if code is not None else True)
                .filter(RefCityTypes.unique_id.like(signature) if signature is not None else True)
                .filter(RefCityTypes.id == id if id != 0 else True)
            )            
            result = self.db.scalars(stmt).first()
            # areas = result.areas
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg, "search" : {"id" : id, "code" : code,"signature" : signature}})

        return result

