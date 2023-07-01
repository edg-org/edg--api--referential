from typing import List
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from api.logs.services.LogService import LogService
from api.ageographical.models.CityModel import CityModel
from api.ageographical.repositories.CityRepo import CityRepo
from api.ageographical.repositories.CityTypeRepo import CityTypeRepo
from api.ageographical.repositories.CityLevelRepo import CityLevelRepo
from api.ageographical.repositories.PrefectureRepo import PrefectureRepo
from api.tools.Helper import build_log, city_basecode, generate_zipcode, generate_code
from api.ageographical.schemas.CitySchema import (
    CityInput,
    CityUpdate,
    CreateCity,
    CitySearchParams
)

#
class CityService:
    city: CityRepo
    log: LogService

    def __init__(
        self, 
        city: CityRepo = Depends(),
        log: LogService = Depends()
    ) -> None:
        self.log = log
        self.city = city

    # get all citys function
    async def list(self, skip: int = 0, limit: int = 100) -> List[CityModel]:
        return self.city.list(skip=skip, limit=limit)

    # get city by id function
    async def get(self, id: int) -> CityModel:
        return self.city.get(id=id)

    # get city by code function
    async def getbycode(self, code: str) -> CityModel:
        return self.city.getbycode(code=code)

    # get city by name function
    async def getbyname(self, name: str) -> CityModel:
        return self.city.getbyname(name=name)

    # get city by name function
    async def getbyzipcode(self, zip_code: str) -> CityModel:
        return self.city.getbyzipcode(zip_code=zip_code)

    # get city by code function
    async def search(self, query_params: CitySearchParams) -> CityModel:
        return self.city.search(query_params=query_params)

    # create city function
    async def create(self, data: List[CityInput]) -> List[CreateCity]:
        step = 0
        zipcode_step = 0
        citylist = []
        prefecture_name = None
        
        for item in data:
            prefecture = PrefectureRepo.getbyname(self.city, item.infos.prefecture)
            count = self.city.checkcityname(prefecture_id = prefecture.id, name=item.infos.name)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"City already registered with name {item.infos.name} inside the prefecture with code {prefecture.code}",
                )
            
            if (prefecture_name is not None) and  (prefecture_name != item.infos.prefecture):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You should only have the list of cities for one prefecture at a time"
                )

            step += 1
            maxzipcode = self.city.maxzipcodebypref(prefecture.id)
            result = generate_code(
                init_codebase=city_basecode(prefecture.code),
                maxcode=self.city.maxcodebypref(prefecture.id),
                step=step
            )
            step = result["step"]
            city_code = result["code"]

            if maxzipcode > 0 :
                zipcode_step += 1
                zipcode_base = maxzipcode
            else:
                zipcode_base = int(prefecture.prefecture_number)*1000
                if (str(item.infos.city_level).lower() == "préfecture"):
                    zipcode_step = 0
                else:
                    if (hasattr(item, "zipcode") is False) or (hasattr(item, "zipcode") and item.zipcode is None):
                        if zipcode_step == 0:
                            zipcode_step = 110
                        else:
                            zipcode_step += 10
                            if (zipcode_step) % 100 == 0:
                                zipcode_step += 10

            count = self.city.countbycode(code=city_code)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"City already registered with code {city_code}",
                )
            
            zipcode = generate_zipcode(zipcode_base, zipcode_step)
            count = self.city.countbyzipcode(zipcode=zipcode)
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"City already registered with zip code {item.zipcode}",
                )
            
            city = CreateCity(
                code = city_code,
                city_type_id = CityTypeRepo.getbyname(self.city, item.infos.city_type).id,
                city_level_id = CityLevelRepo.getbyname(self.city, item.infos.city_level).id,
                prefecture_id = prefecture.id,
                zipcode = str(zipcode),
                infos = item.infos
            )
            citylist.append(city)
            prefecture_name = item.infos.prefecture
            
        return self.city.create(data=citylist)

    # update city function
    async def update(self, code: int, data: CityUpdate) -> CityModel:
        old_data = jsonable_encoder(self.city.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City not found",
            )

        # if (hasattr(data.infos, "city_type") and data.infos.city_type is not None):
        #     data.city_type_id = CityTypeRepo.getbyname(self.city, data.infos.city_type).id
        #
        # if (hasattr(data.infos, "city_level") and data.infos.city_level is not None):
        #     data.city_level_id = CityLevelRepo.getbyname(self.city, data.infos.city_level).id

        prefecture_id, city_type_id, city_level_id = 0, 0, 0
        if (hasattr(data.infos, "prefecture") and data.infos.prefecture is not None):
            try:
                prefecture_id = PrefectureRepo.getbyname(self.city, data.infos.prefecture).id
            except Exception as e:
                raise HTTPException(status_code=404, detail="Prefecture not found")
        req = "CityModel.id != " + str(old_data['id'])

        if (hasattr(data.infos, "city_type") and data.infos.city_type is not None):
            try:
                city_type_id = CityTypeRepo.getbyname(self.city, data.infos.city_type).id
            except Exception as e:
                raise HTTPException(status_code=404, detail="City Type not found")

        if (hasattr(data.infos, "city_level") and data.infos.city_level is not None):
            try:
                city_level_id = CityLevelRepo.getbyname(self.city, data.infos.city_level).id
            except Exception as e:
                raise HTTPException(status_code=404, detail="City Level not found")

        verif = self.city.verif_duplicate(name=data.infos.name, prefecture_id=prefecture_id, req=req)
        if len(verif) != 0:
            raise HTTPException(status_code=405, detail={"msg": "Duplicates are not possible", "name": data.infos.name})

        data = data.dict()
        data.update({"prefecture_id": prefecture_id, "city_type_id": city_type_id, "city_level_id": city_level_id, })

        current_data = jsonable_encoder(self.city.update(code=code, data=data))
        logs = [await build_log(f"/cities/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        await self.log.create(logs)
        return current_data

    # activate or desactivate city function
    async def activate_desactivate(self, code: int, flag: bool) -> None:
        old_data = jsonable_encoder(self.city.getbycode(code=code))
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City not found",
            )
        message = "City desactivated"
        deleted_at = datetime.utcnow().isoformat()
        
        if flag == True:
            deleted_at = None
            message = "City activated"
        
        data = dict(
            is_activated=flag,
            deleted_at = deleted_at
        )
        current_data = jsonable_encoder(self.city.update(code=code, data=data))
        logs = [build_log(f"/cities/{code}", "PUT", "oussou.diakite@gmail.com", old_data, current_data)]
        await self.log.create(logs)
        return HTTPException(status_code=status.HTTP_200_OK, detail=message)
