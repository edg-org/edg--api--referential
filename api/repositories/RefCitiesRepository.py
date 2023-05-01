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
from api.models.RefCitiesModel import RefCities

from api.repositories.RefPrefecturesRepository import RefPrefecturesRepository

from api.schemas.pydantic.RefNaturalRegionsSchema import RefNaturalRegionsSchema, RefNaturalRegionsCreateSchema
from api.schemas.pydantic.RefPrefecturesSchema import RefPrefecturesSchema, RefPrefecturesCreateSchema
from api.schemas.pydantic.RefCitiesSchema import (RefCitiesSchema, RefCitiesCreateSchema, EXAMPLE, RefCitiesUpdateSchema,
EXAMPLE1)

class RefCitiesRepository:
    db: Session
    prefecture_repository : RefPrefecturesRepository

    def __init__(self, prefecture_repository: RefPrefecturesRepository = Depends(), db: Session = Depends(get_db_connection)) -> None:
        self.db = db
        self.prefecture_repository = prefecture_repository

    def create(self, ref_cities: RefCitiesCreateSchema):
        verif_cities = self.verif_duplicate(ref_cities)
        data = ref_cities.dict()
        if len(verif_cities) == 0 :
            try:
                ref_cities = data
                code = self.code_generate(ref_cities['prefecture_id'])
                ref_cities.update({"unique_id" : str(uuid.uuid1().hex)}) # lie a l'adresse MAC du PC uuid4() n'est pas lié
                ref_cities.update({"code" : int(code)})  
                ref_cities['infos'].update({"code": str(code)})

                ref_citie = self.db.execute(insert(RefCities), ref_cities)
                # ref_citie = self.db.execute(insert(RefCities), ref_cities.dict())
                stmt = select(RefCities).where(RefCities.unique_id == ref_cities['unique_id'])
                ref_citie = self.db.scalars(stmt).one()
                self.db.commit()

            except Exception as e:
                raise HTTPException(status_code=400, detail={})

            return ref_citie
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})

    def get(self, id: int, is_activated : bool = True):
        try:
            stmt = select(RefCities).where(RefCities.id == id, RefCities.is_activated == is_activated)
            ref_citie = self.db.scalars(stmt).one()
            # prefectures = ref_citie.prefectures
            # areas = ref_citie.areas
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_citie

    def get_id(self, id : int):
        try:
            ref_citie = self.db.get(RefCities, id)
            if ref_citie ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_citie

    def get_signature(self, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefCities).where(RefCities.unique_id == signature, RefCities.is_activated == is_activated)
            ref_citie = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_citie

    def get_id_and_signature(self, id: int, signature: str, is_activated : bool = True):

        try:
            stmt = select(RefCities).where(RefCities.id == id, RefCities.unique_id == signature, RefCities.is_activated == is_activated)
            ref_citie = self.db.scalars(stmt).one()
        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})

        return ref_citie


    def list(self, skip: int = 0, limit: int = 100):
        try:
            stmt = select(RefCities).where(RefCities.is_activated == True).offset(skip).limit(limit)
            ref_cities = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_cities

    def update(self, ref_cities: RefCitiesUpdateSchema):

        verif_cities = self.verif_duplicate(ref_cities)
        data = ref_cities.dict()
        if len(verif_cities) == 0 :
            cities = data
            cities['infos'].update({"code": str(self.get_code_by_id(cities['id']))})
            try:
                stmt = (
                    update(RefCities)
                    .where(RefCities.id == cities['id'])
                    .values(type_id = cities['type_id'], level_id = cities['level_id'], prefecture_id = cities['prefecture_id'], infos = cities['infos'], updated_at = func.now())
                    # .returning(RefCities)
                )
                ref_citie = self.db.execute(stmt)
                # ref_citie = jsonable_encoder(ref_citie)
                ref_citie = self.db.get(RefCities, cities['id'])

                self.db.commit()

            except Exception as e:
                raise HTTPException(status_code=400, detail={})

            return ref_citie
        else :
            msg = "Duplicates are not possible"
            raise HTTPException(status_code = 405, detail = {"msg" : msg,"data" : data})



    def delete(self, id : int, is_activated : bool = False):
        try:
            stmt = (
                update(RefCities)
                .where(RefCities.id == id)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefCities)
            )
            ref_citie = self.db.execute(stmt)
            # ref_citie = jsonable_encoder(ref_citie)
            ref_citie = self.db.get(RefCities, id)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_citie


    def delete_signature(self, id : int, signature : str, is_activated : bool = False):
        try:
            stmt = (
                update(RefCities)
                .where(RefCities.id == id, RefCities.unique_id == signature)
                .values(is_activated = is_activated, deleted_at = func.now())
                # .returning(RefCities)
            )
            ref_citie = self.db.execute(stmt)
            # ref_citie = jsonable_encoder(ref_citie)
            ref_citie = self.db.get(RefCities, id)
            
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return ref_citie


    def verif_duplicate(self, cities: RefPrefecturesSchema):
        id = cities.id if hasattr(cities, 'id') else 0
        prefecture_id = cities.prefecture_id if hasattr(cities, 'prefecture_id') else 0        
        req ="RefCities.id != " + str(id)
        # name = cities.infos['name'] if 'name' in cities.infos else ""
        name = cities.infos.name if hasattr(cities.infos, 'name') else ""
        try:
            stmt = (
                select(RefCities)
                .filter(RefCities.infos['name'].as_string().ilike(name), RefCities.prefecture_id == prefecture_id)
                .filter(eval(req))
            )
            
            cities = self.db.scalars(stmt).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={})

        return cities

    def get_code_by_id(self, id : int):
        try:
            ref_citie = self.db.get(RefCities, id)
            if ref_citie ==  None : 
                raise 

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg,"id" : id})
        return ref_citie.infos['code']

    def code_generate(self, prefecture_id : int):
        prefecture_code = self.prefecture_repository.get_code_by_id(prefecture_id)

        count_query = select(func.count(RefCities.id)).where(RefCities.prefecture_id == prefecture_id)
        count_result = self.db.execute(count_query).scalar()
        count_result = (int(prefecture_code) * 100) + ((count_result * 10) + 10)
        return count_result

    def get_code(self, code: str, is_activated : bool = True): 
        try:
            stmt = (
                select(RefCities)
                .where(RefCities.is_activated == is_activated)
                .filter(RefCities.infos['code'].as_string().ilike(code))
            )
            
            cities = self.db.scalars(stmt).one()
        except Exception as e:
            raise HTTPException(status_code = 400, detail = {})

        return cities


    def get_items(self, id: Optional[int] = 0, code: Optional[str] = None, signature: Optional[str] = None, is_activated : bool = True):       
        try:
            stmt = (
                select(RefCities)
                .where(RefCities.is_activated == is_activated)
                .filter(RefCities.infos['code'].as_string().ilike(code) if code is not None else True)
                .filter(RefCities.unique_id.like(signature) if signature is not None else True)
                .filter(RefCities.id == id if id != 0 else True)
            )
            
            result = self.db.scalars(stmt).first()

            prefectures = result.prefectures
            areas = result.areas

        except Exception as e:
            msg = "Element not found"
            raise HTTPException(status_code = 406, detail = {"msg" : msg, "search" : {"id" : id, "code" : code,"signature" : signature}})

        return result

