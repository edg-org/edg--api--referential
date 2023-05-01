from typing import List, Optional
import json
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, lazyload
from sqlalchemy import select, insert, update, delete, and_
from fastapi.encoders import jsonable_encoder
import uuid
from sqlalchemy.sql import func

from api.repositories.RefCitiesRepository import RefCitiesRepository

from api.configs.Database import (get_db_connection,)
from api.models.RefNaturalRegionsModel import RefNaturalRegions
from api.models.RefAreasModel import RefAreas
from api.schemas.pydantic.RefAreasSchema import RefAreasSchema, RefAreasCreateSchema, EXAMPLE, RefAreasUpdateSchema, EXAMPLE1

class RefAreasRepository:
    db: Session
    cities_repository : RefCitiesRepository

    def __init__(self, cities_repository: RefCitiesRepository = Depends(), db: Session = Depends(get_db_connection)) -> None:
        self.db = db
        self.cities_repository = cities_repository




    def create(self, ref_areas: RefAreasCreateSchema):
        verif_areas = self.verif_duplicate(ref_areas)
        data = ref_areas.dict()
        if len(verif_areas) == 0 :
            try:
                # # ref_area = self.db.scalars(insert(RefAreas).returning(RefAreas), ref_areas.dict()).first()            
                # unique_id = {"unique_id":str(uuid.uuid1().hex)} # lie a l'adresse MAC du PC uuid4() n'est pas lié
                # ref_areas = data
                # ref_areas.update(unique_id)
                # # ref_areas['unique_id'] = unique_id

                ref_areas = data
                code = self.code_generate(ref_areas['cities_id'])
                ref_areas.update({"unique_id" : str(uuid.uuid1().hex)}) # lie a l'adresse MAC du PC uuid4() n'est pas lié
                ref_areas.update({"code" : int(code)})  
                ref_areas['infos'].update({"code": str(code)})

                ref_area = self.db.execute(insert(RefAreas), ref_areas)
                stmt = select(RefAreas).where(RefAreas.unique_id == ref_areas['unique_id'])
                ref_area = self.db.scalars(stmt).one()
                self.db.commit()

            except Exception as e:
                raise HTTPException(status_code=400, detail={})

            return ref_area
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})

   
    def get(self, id: int, is_activated : bool = True):
        try:
            stmt = select(RefAreas).where(RefAreas.id == id, RefAreas.is_activated == is_activated)
            ref_area = self.db.scalars(stmt).one()
            # cities = ref_area.cities
            # type_areas = ref_area.type_areas
            # agencies = ref_area.agencies

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_area

  
    def get_id(self, id : int):
        try:
            ref_area = self.db.get(RefAreas, id)
            if ref_area ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_area

    def get_signature(self, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefAreas).where(RefAreas.unique_id == signature, RefAreas.is_activated == is_activated)
            ref_area = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_area

    def get_id_and_signature(self, id: int, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefAreas).where(RefAreas.id == id, RefAreas.unique_id == signature, RefAreas.is_activated == is_activated)
            ref_area = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_area

    def list(self, skip: int = 0, limit: int = 100):
        try:
            stmt = select(RefAreas).where(RefAreas.is_activated == True).offset(skip).limit(limit)
            ref_areas = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_areas

    def update(self, ref_areas: RefAreasUpdateSchema):
        verif_areas = self.verif_duplicate(ref_areas)
        data = ref_areas.dict()
        if len(verif_areas) == 0 :
            areas = data
            try:
                stmt = (
                    update(RefAreas)
                    .where(RefAreas.id == areas['id'])
                    .values(cities_id = areas['cities_id'], type_areas_id = areas['type_areas_id'], infos = areas['infos'], updated_at = func.now())
                    # .returning(RefAreas)
                )
                ref_area = self.db.execute(stmt)
                # ref_area = jsonable_encoder(ref_area)
                ref_area = self.get(areas['id'])
                self.db.commit()

            except Exception as e:
                raise HTTPException(status_code=400, detail={})

            return ref_area
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})


    def delete(self, id : int, is_activated : bool = False):
        try:
            stmt = (
                update(RefAreas)
                .where(RefAreas.id == id)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefAreas)
            )
            ref_area = self.db.execute(stmt)
            # ref_area = jsonable_encoder(ref_area)
            ref_area = self.db.get(RefAreas, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_area


    def delete_signature(self, id : int, signature : str, is_activated : bool = False):
        try:
            stmt = (
                update(RefAreas)
                .where(RefAreas.id == id, RefAreas.unique_id == signature)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefAreas)
            )
            ref_area = self.db.execute(stmt)
            # ref_area = jsonable_encoder(ref_area)
            ref_area = self.db.get(RefAreas, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_area

    def verif_duplicate(self, areas: RefAreasSchema):
        id = areas.id if hasattr(areas, 'id') else 0
        cities_id = areas.cities_id if hasattr(areas, 'cities_id') else 0        
        req ="RefAreas.id != " + str(id)
        name = areas.infos.name if hasattr(areas.infos, 'name') else ""
        # name = areas.infos['name'] if 'name' in areas.infos else ""
        try:
            stmt = (
                select(RefAreas)
                .filter(RefAreas.infos['name'].as_string().ilike(name), RefAreas.cities_id == cities_id)
                .filter(eval(req))
            )
            
            areas = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code = 400, detail={})

        return areas


    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, is_activated : bool = True):       
        try:
            stmt = (
                select(RefAreas)
                .where(RefAreas.is_activated == is_activated)
                .filter(RefAreas.infos['code'].as_string().ilike(code) if code is not None else True)
                .filter(RefAreas.unique_id.like(signature) if signature is not None else True)
                .filter(RefAreas.id == id if id != 0 else True)
            )
            
            result = self.db.scalars(stmt).first()

            cities = result.cities
            type_areas = result.type_areas
            agencies = result.agencies

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg, "search" : {"id" : id, "code" : code,"signature" : signature}})

        return result


    def code_generate(self, cities_id : int):
        cities_code = self.cities_repository.get_code_by_id(cities_id)

        count_query = select(func.count(RefAreas.id)).where(RefAreas.cities_id == cities_id)
        count_result = self.db.execute(count_query).scalar()
        count_result = (int(cities_code) * 100) + (count_result + 1)
        # count_result = (int(cities_code) * 100) + ((count_result * 10) + 1) 
        return count_result
