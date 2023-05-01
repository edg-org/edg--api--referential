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
from api.models.RefTypeAreasModel import RefTypeAreas
from api.schemas.pydantic.RefTypeAreasSchema import (RefTypeAreasSchema, RefTypeAreasCreateSchema, EXAMPLE, 
RefTypeAreasUpdateSchema, EXAMPLE1)

class RefTypeAreasRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self, ref_type_areas: RefTypeAreasCreateSchema):
        verif_type_areas = self.verif_duplicate(ref_type_areas)
        data = ref_type_areas.dict()

        if len(verif_type_areas) == 0 :
            try:
                unique_id = {"unique_id":str(uuid.uuid1().hex)} # lie a l'adresse MAC du PC uuid4() n'est pas lié
                ref_type_areas = data
                ref_type_areas.update(unique_id)
                # ref_type_areas['unique_id'] = unique_id

                ref_type_area = self.db.execute(insert(RefTypeAreas), ref_type_areas)
                # ref_type_area = self.db.execute(insert(RefTypeAreas), ref_type_areas.dict())
                stmt = select(RefTypeAreas).where(RefTypeAreas.unique_id == ref_type_areas['unique_id'])
                ref_type_area = self.db.scalars(stmt).one()
                self.db.commit()

            except Exception as e:
                raise HTTPException(status_code=400, detail={})

            return ref_type_area
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})

    def get(self, id: int, is_activated : bool = True):
        try:
            stmt = select(RefTypeAreas).where(RefTypeAreas.id == id, RefTypeAreas.is_activated == is_activated)
            ref_type_area = self.db.scalars(stmt).one()
            # areas = ref_type_area.areas
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_type_area

    def get_id(self, id : int):
        try:
            ref_type_area = self.db.get(RefTypeAreas, id)
            if ref_type_area ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_type_area

    def get_signature(self, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefTypeAreas).where(RefTypeAreas.unique_id == signature, RefTypeAreas.is_activated == is_activated)
            ref_type_area = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_type_area

    def get_id_and_signature(self, id: int, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefTypeAreas).where(RefTypeAreas.id == id, RefTypeAreas.unique_id == signature, RefTypeAreas.is_activated == is_activated)
            ref_type_area = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_type_area



    def list(self, skip: int = 0, limit: int = 100):
        try:
            stmt = select(RefTypeAreas).where(RefTypeAreas.is_activated == True).offset(skip).limit(limit)
            ref_type_areas = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_type_areas

    def update(self, ref_type_areas: RefTypeAreasUpdateSchema):
        verif_type_areas = self.verif_duplicate(ref_type_areas)
        data = ref_type_areas.dict()
        if len(verif_type_areas) == 0 :
            type_areas = data
            try:
                stmt = (
                    update(RefTypeAreas)
                    .where(RefTypeAreas.id == type_areas['id'])
                    .values(name = type_areas['name'], infos = type_areas['infos'], updated_at = func.now())
                    # .returning(RefTypeAreas)
                )
                ref_type_area = self.db.execute(stmt)
                ref_type_area = self.db.get(RefTypeAreas, type_areas['id'])

                self.db.commit()
            except Exception as e:
                raise HTTPException(status_code = 400, detail = {})

            return ref_type_area
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})



    def delete(self, id : int, is_activated : bool = False):
        try:
            stmt = (
                update(RefTypeAreas)
                .where(RefTypeAreas.id == id)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefTypeAreas)
            )
            ref_type_area = self.db.execute(stmt)
            # ref_type_area = jsonable_encoder(ref_type_area)
            ref_type_area = self.db.get(RefTypeAreas, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_type_area


    def delete_signature(self, id : int, signature : str, is_activated : bool = False):
        try:
            stmt = (
                update(RefTypeAreas)
                .where(RefTypeAreas.id == id, RefTypeAreas.unique_id == signature)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefTypeAreas)
            )
            ref_type_area = self.db.execute(stmt)
            # ref_type_area = jsonable_encoder(ref_type_area)
            ref_type_area = self.db.get(RefTypeAreas, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_type_area

    def verif_duplicate(self, type_areas: RefTypeAreasSchema):
        id = type_areas.id if hasattr(type_areas, 'id') else 0
        req ="RefTypeAreas.id != " + str(id)

        name = type_areas.name if hasattr(type_areas, 'name') else ""        
        try:
            stmt = (
                select(RefTypeAreas)
                .filter(RefTypeAreas.name.ilike(name))
                .filter(eval(req))
            )
            
            type_areas = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return type_areas

    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, is_activated : bool = True):       
        try:
            stmt = (
                select(RefTypeAreas)
                .where(RefTypeAreas.is_activated == is_activated)
                # .filter(RefTypeAreas.infos['code'].as_string().ilike(code) if code is not None else True)
                .filter(RefTypeAreas.unique_id.like(signature) if signature is not None else True)
                .filter(RefTypeAreas.id == id if id != 0 else True)
            )
            
            result = self.db.scalars(stmt).first()

            areas = result.areas

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg, "search" : {"id" : id, "code" : code,"signature" : signature}})

        return result

